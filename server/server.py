from context import Context
from message import Message
from operator import methodcaller
from state import Connected, GoingOut
from threading import Thread
import pickle
import socket

class Server:
    def __init__(self, sock=None):
        self.clients = {}
        self.transactions = {}

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def create_socket(self, host, port):
        self.sock.bind((host, port))
        self.sock.listen()

    def waiting_connections(self):
        print('Waiting connections!')
        return self.sock.accept()

    def handle_connection(self, socket):
        try:
            context = Context(Connected(), socket, self)

            while (not isinstance(context.state, GoingOut)):
                message = pickle.loads(socket.recv(1024))
                print(f"-> Message received: \n{message}")
                operation = message.operation

                if hasattr (context, operation.lower()):
                    methodcaller(operation.lower(), message)(context)
                else:
                    context.default(message)

        except Exception as e:
            print('ERROR:', e)

        finally:
            self.close_socket(socket)

    def close_socket(self, socket):
        socket.close()
        print('Connection closed!')

    def find_user(self, username):
        return self.clients.get(username)

    def find_transaction(self, transaction_id):
        return self.transactions.get(transaction_id)

if __name__ == '__main__':
    try:
        server = Server()
        server.create_socket('127.0.0.1', 55555)
        print('Server initialized!')

        while True:
            conn, addr = server.waiting_connections()
            print('Client connected!')
            thread = Thread(target=server.handle_connection,args=(conn,))
            thread.start()

    except Exception as e:
        raise e
