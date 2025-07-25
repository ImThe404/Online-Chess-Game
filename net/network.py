import socket
import threading
import json

class NetworkBase:
    def __init__(self):
        self.on_message = None
        self.connected = False

    def send(self, data):
        try:
            message = json.dumps(data) + '\n'
            self.conn.sendall(message.encode())
        except Exception as e:
            print("Erreur d'envoi:", e)

    def _listen(self):
        buffer = ""
        while self.connected:
            try:
                data = self.conn.recv(1024)
                if not data:
                    print("Connexion perdue.")
                    self.connected = False
                    break
                buffer += data.decode()
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    message = json.loads(line)
                    if self.on_message:
                        self.on_message(message)
            except Exception as e:
                print("Erreur de réception:", e)
                self.connected = False
                break

class NetworkServer(NetworkBase):
    def __init__(self, host='0.0.0.0', port=12345):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        print("En attente de connexion...")
        self.conn, addr = self.sock.accept()
        print(f"Client connecté depuis {addr}")
        self.connected = True
        threading.Thread(target=self._listen, daemon=True).start()

class NetworkClient(NetworkBase):
    def __init__(self, host='localhost', port=12345):
        super().__init__()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conn.connect((host, port))
            print("Connecté au serveur")
            self.connected = True
            threading.Thread(target=self._listen, daemon=True).start()
        except Exception as e:
            print("Connexion échouée:", e)
