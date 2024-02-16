import json
import socket
from question_repo.question_repo import QuestionRepo


class Server:
    def __init__(self) -> None:
        self.question_repo = QuestionRepo()

        server_address = (self.get_ip_address(), 58008)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(server_address)
        self.server_socket.listen(1)

        print("server is listening...")

        self.connection, self.client_address = self.server_socket.accept()

    def run(self):
        print(self.question_repo.get_new_question())

    def get_ip_address(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
