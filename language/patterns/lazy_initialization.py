# Tactic of delaying the creation of an object, the calculation of a value, or some other expensive process until
# the first time it is needed. This pattern appears in the GoF catalog as "virtual proxy", an implementation strategy
# for the Proxy pattern.
#
# https://en.wikipedia.org/wiki/Lazy_initialization


class Fruit:
    def __init__(self, item):
        self.item = item


class Fruits:
    def __init__(self):
        self.items = {}

    def get_fruit(self, item):
        if item not in self.items:
            self.items[item] = Fruit(item)

        return self.items[item]


if __name__ == '__main__':
    fruits = Fruits()
    print(fruits.get_fruit('Apple'))
    print(fruits.get_fruit('Lime'))
