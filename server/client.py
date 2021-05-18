from threading import Semaphore

class Client:

    def __init__(self):
        self.username = None
        self.password = None
        self.wallet = None
        self.semaphore = Semaphore()
