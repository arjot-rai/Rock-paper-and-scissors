import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "172.16.1.67"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(data.encode())
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)

