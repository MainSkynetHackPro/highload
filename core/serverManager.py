import socket

from core.serverThread import ServerThread


class ServerManager:
    def __init__(self, port, thread_count, document_root):

        self.port = int(port)
        self.thread_count = int(thread_count)
        self.document_root = document_root

        self.threads = []

    def run(self):

        tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcpServer.bind(('0.0.0.0', self.port))
        tcpServer.listen(self.thread_count)
        # tcpServer.setblocking(False)

        for i in range(self.thread_count):
            thread = ServerThread(tcpServer, self.document_root)
            self.threads.append(thread)
            thread.run()

