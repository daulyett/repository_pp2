class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Some sound"


class Dog(Animal):
    def speak(self):
        return "Bark"


dog = Dog("Buddy")
print(dog.name)
print(dog.speak())