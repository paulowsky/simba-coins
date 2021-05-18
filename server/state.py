from abc import ABC, abstractmethod
from wallet import Wallet
from message import Message
from client import Client
import pickle

class State(ABC):

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        self._context = context

    @abstractmethod
    def signup(self, message):
        pass

    @abstractmethod
    def login(self, message):
        pass

    @abstractmethod
    def ext(self, message):
        pass

    @abstractmethod
    def dep(self, message):
        pass

    @abstractmethod
    def saq(self, message):
        pass

    @abstractmethod
    def transf(self, message):
        pass

    @abstractmethod
    def conf(self, message):
        pass

    @abstractmethod
    def list(self, message):
        pass

    @abstractmethod
    def delete(self, message):
        pass

    @abstractmethod
    def logout(self, message):
        pass

    @abstractmethod
    def sair(self, message):
        pass

    def default(self, message):
        response = Message(message)
        response.status = 401
        response.params['res'] = 'Invalid operation for state!'
        self.context.socket.send(pickle.dumps(response))

class Connected(State):
    def signup(self, message):
        response = Message('SIGNUPREPLY')
        try:
            username = message.params['user']
            password = message.params['pass']

            if not self.context.server.find_user(username):
                response.status = 200
                response.params['res'] = 'User Registered! You are now Authenticated!'
                self.context.client = Client()
                self.context.client.username = username
                self.context.client.password = password
                self.context.client.wallet = Wallet(username)
                self.context.server.clients[username] = self.context.client
                self.context.transition_to(Authenticated())
            else:
                response.status = 400
                response.params['res'] = 'This username already exists!'
        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def login(self, message):
        response = Message('LOGINREPLY')
        try:
            username = message.params['user']
            password = message.params['pass']

            client = self.context.server.find_user(username)
            if client and client.password == password:
                response.status = 200
                response.params['res'] = 'LogIn Successfully!'
                self.context.client = client
                self.context.transition_to(Authenticated())
            else:
                response.status = 400
                response.params['res'] = 'Invalid Username or Password!'
        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def ext(self, message):
        self.default('EXTREPLY')

    def dep(self, message):
        self.default('DEPREPLY')

    def saq(self, message):
        self.default('SAQREPLY')

    def transf(self, message):
        self.default('TRANSFREPLY')

    def conf(self, message):
        self.default('CONFREPLY')

    def list(self, message):
        self.default('LISTREPLY')

    def delete(self, message):
        self.default('DELETEREPLY')

    def logout(self, message):
        self.default('LOGOUTREPLY')

    def sair(self, message):
        response = Message('SAIRREPLY')
        response.status = 200
        response.params['res'] = 'Connection is going to close!'
        self.context.socket.send(pickle.dumps(response))

class Authenticated(State):
    def signup(self, message):
        self.default('SIGNUPREPLY')

    def login(self, message):
        self.default('LOGINREPLY')

    def ext(self, message):
        response = Message('EXTREPLY')
        try:
            response.status = 200
            response.params['balance'] = self.context.client.wallet.balance

        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def dep(self, message):
        response = Message('DEPREPLY')
        try:
            quantity = float(message.params['qtd'])

            if quantity:
                balance_before = self.context.client.wallet.balance
                self.context.client.wallet.balance += quantity
                response.status = 200
                response.params['balancebefore'] = balance_before
                response.params['balanceafter'] = self.context.client.wallet.balance

            else:
                response.status = 400
                response.params['res'] = 'Param qtd invalid!'

        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def saq(self, message):
        response = Message('SAQREPLY')
        try:
            quantity = float(message.params['qtd'])

            if not quantity:
                response.status = 400
                response.params['res'] = 'Param qtd invalid!'

            elif self.context.client.wallet.balance < quantity:
                response.status = 400
                response.params['res'] = 'Balance insufficient!'

            else:
                balance_before = self.context.client.wallet.balance
                self.context.client.wallet.balance -= quantity
                response.status = 200
                response.params['balancebefore'] = balance_before
                response.params['balanceafter'] = self.context.client.wallet.balance

        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def transf(self, message):
        response = Message('TRANSFREPLY')
        try:
            quantity = float(message.params['amount'])
            client = self.context.server.find_user(message.params['destiny'])

            if not quantity or not client:
                response.status = 400
                response.params['res'] = 'Param amount or destiny invalid!'

            elif self.context.client.wallet.balance < quantity:
                response.status = 400
                response.params['res'] = 'Balance insufficient!'

            else:
                id = len(self.context.server.transactions)
                self.context.server.transactions[id] = \
                    {
                        'origin': self.context.client,
                        'destiny': client,
                        'amount': quantity,
                        'status': 'pending'
                    }

                self.context.client.semaphore.acquire()
                self.context.client.semaphore.acquire()
                response.status = 200
                transf = self.context.server.transactions[id]

                if transf['status'] == 'approved':
                    self.context.client.wallet.balance -= quantity
                    client.wallet.balance += quantity
                    response.params['res'] = 'Transaction approved!'
                    response.params['balanceafter'] = self.context.client.wallet.balance
                elif transf['status'] == 'reproved':
                    response.params['res'] = 'Transaction reproved!'
                    response.params['balanceafter'] = self.context.client.wallet.balance

                self.context.client.semaphore.release()

        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def conf(self, message):
        response = Message('CONFREPLY')
        try:
            transf_id = int(message.params['idtransf'])
            status = message.params['status']
            transf = self.context.server.transactions[transf_id]

            if transf:
                if status.upper() == 'APPROVED' or status.upper() == 'REPROVED':
                    if self.context.client.username == transf['destiny'].username:
                        if transf['status'] == 'pending':
                            response.status = 200
                            if status.upper() == 'APPROVED':
                                response.params['res'] = 'Transaction approved!'
                            elif status.upper() == 'REPROVED':
                                response.params['res'] = 'Transaction reproved!'
                            transf['status'] = status.lower()
                            transf['origin'].semaphore.release()
                        else:
                            response.status = 400
                            response.params['res'] = 'This transaction is already confirmed!'
                    else:
                        response.status = 400
                        response.params['res'] = 'This transaction is not for you!'
                else:
                    response.status = 400
                    response.params['res'] = 'Invalid status!'
            else:
                response.status = 400
                response.params['res'] = 'This transaction do not exists!'
        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def list(self, message):
        response = Message('LISTREPLY')
        try:
            wallets = [str(c.wallet) for c in self.context.server.clients.values()]
            response.status = 200
            response.params['res'] = '\n'.join(wallets)

        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def delete(self, message):
        response = Message('DELETEREPLY')
        try:
            del self.context.server.clients[self.context.client.username]
            del self.context.client
            response.status = 200
            response.params['res'] = 'Delete Successfully!'
            self.context.transition_to(Connected())

        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def logout(self, message):
        response = Message('LOGOUTREPLY')
        try:
            response.status = 200
            response.params['res'] = 'Logout Successfully!'
            self.context.transition_to(Connected())
        except Exception as e:
            response.status = 500
            response.params['res'] = 'Internal Server Error!'

        self.context.socket.send(pickle.dumps(response))

    def sair(self, message):
        response = Message('SAIRREPLY')
        response.status = 200
        response.params['res'] = 'Connection is going to close!'
        self.context.socket.send(pickle.dumps(response))

class GoingOut(State):
    def signup(self, message):
        pass

    def login(self, message):
        pass

    def ext(self, message):
        pass

    def dep(self, message):
        pass

    def saq(self, message):
        pass

    def transf(self, message):
        pass

    def conf(self, message):
        pass

    def list(self, message):
        pass

    def delete(self, message):
        pass

    def logout(self, message):
        pass

    def sair(self, message):
        pass
