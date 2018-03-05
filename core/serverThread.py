from threading import Thread

import select


class ServerThread(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            try:
                conn, addr = self.socket.accept()
                data = conn.recv(2048)
                conn.send('ok')
                conn.close()
            except:
                pass


