from message import Message
import pickle
import uuid

class Context:
    state = None
    client = None

    def __init__(self, state, socket, server):
        self.transition_to(state)
        self.socket = socket
        self.id = uuid.uuid4()
        self.server = server

    def transition_to(self, state):
        print(f"Context transition to state: {type(state).__name__}")
        self.state = state
        self.state.context = self

    def signup(self, message):
        self.state.signup(message)

    def login(self, message):
        self.state.login(message)

    def ext(self, message):
        self.state.ext(message)

    def dep(self, message):
        self.state.dep(message)

    def saq(self, message):
        self.state.saq(message)

    def transf(self, message):
        self.state.transf(message)

    def list(self, message):
        self.state.list(message)

    def delete(self, message):
        self.state.delete(message)

    def logout(self, message):
        self.state.logout(message)

    def sair(self, message):
        self.state.sair(message)

    def default(self, message):
        response = Message(f"{message.operation}REPLY")
        response.status = 401
        response.params['res'] = 'Invalid operation for state!'
        self.socket.send(pickle.dumps(response))
