# Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat
# individual objects and compositions of objects uniformly.
#
# https://en.wikipedia.org/wiki/Composite_pattern

from abc import ABC, abstractmethod


class Graphic(ABC):
    @abstractmethod
    def print(self):
        raise NotImplementedError()


class CompositeGraphic(Graphic):
    """
    The main feature of the composition is that this class can hold instances 
    of other classes. In the __init__ a container of objects is initialized,
    in add new object is added to the container, in remove the object is 
    deleted from the container, print method iterates over all the objects in
    the container.
    """

    def __init__(self):
        self.graphics = []

    def print(self):
        for graphic in self.graphics:
            graphic.print()

    def add(self, graphic):
        self.graphics.append(graphic)

    def remove(self, graphic):
        self.graphics.remove(graphic)


class Ellipse(Graphic):
    def __init__(self, name):
        self.name = name

    def print(self):
        print("Ellipse:", self.name)


ellipse1 = Ellipse("1")
ellipse2 = Ellipse("2")
ellipse3 = Ellipse("3")
ellipse4 = Ellipse("4")

graphic1 = CompositeGraphic()
graphic2 = CompositeGraphic()
graphic3 = CompositeGraphic()

graphic2.add(ellipse1)
graphic2.add(ellipse2)
graphic2.add(ellipse3)

graphic3.add(ellipse4)

graphic1.add(graphic2)
graphic1.add(graphic3)

graphic1.print()
