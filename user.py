class User:
    def __init__(self, uid, eta1, eta2, operation, age):
        self.uid = uid
        self.eta1 = eta1
        self.eta2 = eta2
        self.operation = operation
        self.age = age
        self.no = None
        self.time = None
        self.sube = None

    def get_eta(self):
        if self.sube is '1':
            return self.eta1
        return self.eta2