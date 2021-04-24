import random

class Wallet:

    def __init__(self, username):
        self.id = random.randint(1, 9999)
        self.balance = 0.0
        self.owner = username

    def __str__(self):
        return f"Wallet: {self.id} - owner: {self.owner}"
