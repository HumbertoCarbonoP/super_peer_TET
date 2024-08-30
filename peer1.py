from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

files = {}

neighbour_peers = []

DIRECTORY = '/home/hcarbono/Documentos/super_peer_TET/files_peer_1/'

for filename in os.listdir(DIRECTORY):
        filepath = os.path.join(DIRECTORY, filename)
        if os.path.isfile(filepath):
            files[filename] = filepath

print(files)

@app.route('/search_file', methods=['GET'])
def search_file():
    filename = request.args.get('filename')
    if filename in files:
        return jsonify({"found": True, "filepath": files[filename]})
    else:
        return jsonify({"found": False}), 404

@app.route('/login', methods=['POST'])
def login():
    try:
        response = requests.post(f"http://localhost:5000/register_peer", json={"peer_address": "localhost:5001"})
        if response.status_code == 200:
            data = response.json()
            neighbour_peers = data.get('registered_peers').split(',')
            print("Vecinos: ", neighbour_peers)
            return jsonify({"message": "Login successful"}), 200
    except:
        return jsonify({"message": "Failed to login"}), 500
    
@app.route('/update_neighbors', methods=['PUT'])
def update_neighbors():
    print("Vecinos viejos: ", neighbour_peers)
    data = request.get_json()
    new_neighbours = data.get('registered_peers').split(',')
    neighbour_peers.clear()
    neighbour_peers.extend(new_neighbours)
    print("Vecinos nuevos: ", neighbour_peers)
    return jsonify({"message": "Neighbors updated successfully"}), 200
    
@app.route('/')
def home():
    return "You can register yourself as a peer at http://localhost:5001/login"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
