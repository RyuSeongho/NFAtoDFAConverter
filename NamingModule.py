# NamingModule.py
class NamingModule:
    def __init__(self, print_type='default'):
        self.counter = 0
        self.type = print_type

    def get_name(self):
        if self.type == 'alphabet':
            name = chr(ord('A') + self.counter)
        else:
            name = f'q{str(self.counter).zfill(3)}'

        self.counter += 1
        return name
