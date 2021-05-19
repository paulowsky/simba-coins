from message import Message
import pickle
import socket

class Client:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def handleConnection(self):
        try:
            left = False

            while (not left):
                print("""
                Operations:
                signup: register and auth
                login: auth
                ext: statement
                dep: deposit
                saq: withdraw
                transf: transfer
                conf: confirm transfter you have received
                list: list wallets
                del: delete wallet
                logout: logout
                sair: close communication
                """)
                operation = input('Type the operation:')

                if operation != None:
                    message = Message(operation)

                    if operation.upper() == 'SIGNUP' or operation.upper() == 'LOGIN':
                        message.params['user'] = input('Type the username:')
                        message.params['pass'] = input('Type the password:')

                    elif operation.upper() == 'DEP':
                        message.params['qtd'] = input('Type the quantity you want to deposit:')

                    elif operation.upper() == 'SAQ':
                        message.params['qtd'] = input('Type the quantity you want to get:')

                    elif operation.upper() == 'TRANSF':
                        message.params['amount'] = input('Type the quantity you want to transfer:')
                        message.params['destiny'] = input('Type the username of the recipient wallet owner:')
                        print('Waiting confirmation...')

                    elif operation.upper() == 'CONF':
                        message.params['idtransf'] = input('Type the id of the transaction you want to confirm:')
                        message.params['status'] = input('Type the status you want to confirm:')

                    elif operation.upper() == 'SAIR':
                        left = True

                    self.sock.send(pickle.dumps(message))
                    response = pickle.loads(self.sock.recv(1024))
                    print(f"-> Message received: \n{response}")

                else:
                    print('Operação inválida!')

        except Exception as e:
            print('Error', e)

        finally:
            self.close_socket(self.sock)

    def close_socket(self, socket):
        socket.close()
        print('Connection closed!')

if __name__ == '__main__':
    try:
        client = Client()
        print('Client initialized!')
        client.connect('127.0.0.1', 55555)
        print('Connection established!')
        client.handleConnection()
    except Exception as e:
        print('ERROR e: ', e)
