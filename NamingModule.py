# NamingModule.py
class NamingModule:
    def __init__(self):
        self.counter = ord('@')

    def get_name(self):
        self.counter += 1
        return chr(self.counter)
