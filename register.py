from flask import Flask, request, jsonify, after_this_request
import requests
import time
import threading

app = Flask(__name__)

peers = []

def update_peers_neighbors(peer_address):
    print(f"Updating neighbors for peer {peer_address}")
    for peer in peers:
        if peer != peer_address:
            try:
                print("URL:", f"http://{peer}/update_neighbors")
                response = requests.put(f"http://{peer}/update_neighbors", json={"registered_peers": peer_address})
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error updating peer {peer}: {e}")
                
# def update_peers_neighbors_async(peer_address):
#     thread = threading.Thread(target=update_peers_neighbors, args=(peer_address,))
#     thread.daemon = True
#     thread.start()

@app.route('/register_peer', methods=['POST'])
def register_peer():
    data = request.get_json()
    peer_address = data.get('peer_address')
    if peer_address not in peers:
        peers.append(peer_address)
        returning_peers = ""
        for peer in peers:
            if peer != peer_address:
                returning_peers += f"{peer},"

        update_peers_neighbors(peer_address)

        return jsonify({"message": f"Peer {peer_address} registered successfully",
                        "registered_peers": f"{returning_peers[0:-1]}"}), 200
    else:
        return jsonify({"message": f"Peer {peer_address} already registered"}), 400

@app.route('/')
def home():
    return "You can register your peer in /register_peer"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
