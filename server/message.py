class Message:
    def __init__(self, operation):
        self.operation = operation
        self.params = {}
        self.status = None

    def __str__(self):
        m = f"Operation: {self.operation}"\
        + f"\nStatus: {self.status}"\
        + f"\nParams:"
        for key, value in self.params.items():
            m += f"\n-> [{key}]: {value}"
        return m
