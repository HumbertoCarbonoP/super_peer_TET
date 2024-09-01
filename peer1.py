from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

local_files = {}

neighbors_peers_files = {}

DIRECTORY = './files_peer_1/'

for filename in os.listdir(DIRECTORY):
        filepath = os.path.join(DIRECTORY, filename)
        if os.path.isfile(filepath):
            local_files[filename] = filepath

@app.route('/search_file', methods=['GET'])
def search_file():
    filename = request.args.get('filename')
    if filename in local_files:
        return jsonify({"found": True, "filepath": local_files[filename]})
    else:
        for neighbor in neighbors_peers_files:
            for file in neighbors_peers_files[neighbor]:
                if file == filename:
                    try:
                        response = requests.get(f"http://{neighbor}/download_file?filename={filename}")
                        response.raise_for_status()
                        if response.status_code == 200:
                            return jsonify({"found": True, "filepath": response.json().get('filepath')}), 200
                    except requests.exceptions.RequestException as e:
                        print(f"Failed to download file from {neighbor}: {e}")
                        continue
        return jsonify({"found": False}), 404
    
@app.route("/download_file", methods=["GET"])
def download_file():
    local_files = {}
    for filename in os.listdir(DIRECTORY):
        filepath = os.path.join(DIRECTORY, filename)
        if os.path.isfile(filepath):
            local_files[filename] = filepath
    filename = request.args.get('filename')
    if filename in local_files:
        return jsonify({"found": True, "filepath": local_files[filename]}), 200
    else:
        return jsonify({"found": False}), 404

@app.route('/login', methods=['POST'])
def login():
    try:
        response = requests.post(f"http://localhost:5000/register_peer", json={"peer_address": "localhost:5001", "peer_files": local_files})
        if response.status_code == 200:
            data = response.json()
            neighbor_peers = data.get('registered_peers')
            for peer in neighbor_peers.keys():
                if(peer != "localhost:5001"):
                    neighbors_peers_files[peer] = neighbor_peers[peer]
            return jsonify({"message": "Login successful"}), 200
    except Exception as e:
        return jsonify({"message": "Failed to login"}), 500
    
@app.route('/update_neighbors', methods=['PUT'])
def update_neighbors():
    data = request.get_json()
    new_neighbors = data.get('registered_peers')
    for new_neighbor in new_neighbors.keys():
        if new_neighbor not in neighbors_peers_files.keys() and new_neighbor != 'localhost:5001':
            neighbors_peers_files[new_neighbor] = new_neighbors[new_neighbor]
    return jsonify({"message": "Neighbors updated successfully"}), 200
    
@app.route('/')
def home():
    return "You can register yourself as a peer at http://localhost:5001/login"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
