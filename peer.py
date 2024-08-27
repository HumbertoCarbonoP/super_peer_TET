from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Diccionario para simular la base de datos de archivos
files = {}

# Directorio donde se buscarán los archivos
DIRECTORY = '/path/to/your/directory'

# Endpoint para registrar un archivo en este peer
@app.route('/register_file', methods=['POST'])
def register_file():
    data = request.get_json()
    filename = data.get('filename')
    filepath = os.path.join(DIRECTORY, filename)
    files[filename] = filepath
    return jsonify({"message": f"File {filename} registered successfully", "filepath": filepath}), 201

# Endpoint para buscar un archivo en este peer
@app.route('/search_file', methods=['GET'])
def search_file():
    filename = request.args.get('filename')
    if filename in files:
        return jsonify({"found": True, "filepath": files[filename]})
    else:
        return jsonify({"found": False}), 404

# Endpoint para detectar la llegada de un nuevo peer
@app.route('/peer_detected', methods=['POST'])
def peer_detected():
    data = request.get_json()
    new_peer = data.get('peer_address')
    print(f"New peer detected: {new_peer}")
    # Aquí podrías registrar el nuevo peer en una lista o base de datos
    return jsonify({"message": "Peer detected", "peer_address": new_peer}), 200

# Cliente: Notificar a otro peer que este peer está activo
def notify_peer(peer_address):
    try:
        response = requests.post(f"http://{peer_address}/peer_detected", json={"peer_address": request.host_url})
        if response.status_code == 200:
            print(f"Successfully notified peer at {peer_address}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to notify peer at {peer_address}: {e}")

# Simular la detección de un peer
def simulate_peer_detection(peer_address):
    notify_peer(peer_address)
    
    
@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
