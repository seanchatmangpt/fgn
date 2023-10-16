def greet(name):
    return f'Hello, {name}!'

class Person:

    def __init__(self, name):
        self.name = name

    def introduce(self):
        return f'My name is {self.name}'