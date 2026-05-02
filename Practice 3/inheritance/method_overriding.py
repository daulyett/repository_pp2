class Bird:
    def fly(self):
        return "Flying"


class Penguin(Bird):
    def fly(self):
        return "Cannot fly"


bird = Bird()
penguin = Penguin()

print(bird.fly())
print(penguin.fly())