import socket
from threading import Thread

from core.requestHandler import RequestHandler


class ServerThread(Thread):

    def __init__(self, socket, document_root):
        Thread.__init__(self)
        self.socket = socket
        self.document_root = document_root

    def run(self):
        while True:
            try:
                self.connection_loop()
            except socket.error as e:
                print(e)

    def connection_loop(self):
        conn, adr = self.socket.accept()
        request = conn.recv(1024)

        if len(request.strip()) == 0:
            conn.close()
            return
        conn.sendall(RequestHandler(request, self.document_root).get_response())
        conn.close()


