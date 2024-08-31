from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

files = {}
neighbour_peers = set()
shared_files = {}  # Diccionario global de archivos compartidos

# Configuración dinámica del peer
def initialize_peer(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            files[filename] = filepath
            shared_files[filename] = filepath  # Inicialmente los archivos locales son los compartidos

@app.route('/search_file', methods=['GET'])
def search_file():
    filename = request.args.get('filename')
    if filename in shared_files:
        return jsonify({"found": True, "filepath": shared_files[filename]})
    return jsonify({"found": False}), 404

@app.route('/register_peer', methods=['POST'])
def register_peer():
    data = request.get_json()
    peer_address = data.get('peer_address')
    peer_files = data.get('peer_files')
    
    if peer_address not in neighbour_peers:
        neighbour_peers.add(peer_address)
        
        # Actualizar el diccionario global de archivos compartidos
        shared_files.update(peer_files)

        # Forzar sincronización: Solicitar la lista completa de archivos a los otros peers
        for peer in neighbour_peers:
            if peer != peer_address:
                try:
                    response = requests.get(f"http://{peer}/get_shared_files")
                    if response.status_code == 200:
                        shared_files.update(response.json())
                except requests.exceptions.RequestException as e:
                    print(f"Error synchronizing with peer {peer}: {e}")

        print(f"Peer {peer_address} registered with files: {peer_files}")
        return jsonify({"message": "Peer registered successfully"}), 200
    else:
        return jsonify({"message": "Peer already registered"}), 400

@app.route('/update_shared_files', methods=['POST'])
def update_shared_files():
    global shared_files
    data = request.get_json()
    new_shared_files = data.get('shared_files', {})
    
    # Actualizar el diccionario global de archivos compartidos
    shared_files.update(new_shared_files)
    
    print(f"Updated shared files: {shared_files}")
    return jsonify({"message": "Shared files updated successfully"}), 200

@app.route('/get_shared_files', methods=['GET'])
def get_shared_files():
    return jsonify(shared_files)

@app.route('/')
def home():
    return "Peer is running"

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Start a P2P peer")
    parser.add_argument('--port', type=int, required=True, help="Port number to run the peer on")
    parser.add_argument('--directory', type=str, required=True, help="Directory where peer's files are stored")
    
    args = parser.parse_args()

    # Inicializar el peer con el directorio especificado
    initialize_peer(args.directory)

    # Ejecutar la aplicación Flask en el puerto especificado
    app.run(host='0.0.0.0', port=args.port)
