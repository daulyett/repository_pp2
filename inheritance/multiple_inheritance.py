class Father:
    def skill(self):
        return "Gardening"


class Mother:
    def skill(self):
        return "Cooking"


class Child(Father, Mother):
    pass


child = Child()
print(child.skill())