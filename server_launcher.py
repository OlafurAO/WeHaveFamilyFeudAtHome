import sys

from server.server import Server

if __name__ == '__main__':
  if len(sys.argv) > 1:
    password = sys.argv[1]
    server = Server()
    server.init_server(password)
