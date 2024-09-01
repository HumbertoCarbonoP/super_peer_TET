from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

peers_files = {}

def update_peers_neighbors(peer_address):
    for peer in peers_files.keys():
        if peer != peer_address:
            try:
                response = requests.put(f"http://{peer}/update_neighbors", json={"registered_peers": peers_files})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error updating peer {peer}: {e}")

@app.route('/register_peer', methods=['POST'])
def register_peer():
    data = request.get_json()
    peer_address = data.get('peer_address')
    peer_files = data.get('peer_files')
    if peer_address not in peers_files.keys():
        peers_files[peer_address] = peer_files
        update_peers_neighbors(peer_address)
        return jsonify({"message": f"Peer {peer_address} registered successfully",
                        "registered_peers": peers_files}), 200
    else:
        return jsonify({"message": f"Peer {peer_address} already registered"}), 400

@app.route('/')
def home():
    return "You can register your peer in /register_peer"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
