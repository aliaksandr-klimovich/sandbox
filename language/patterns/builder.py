# Separate the construction of a complex object from its representation, allowing the same construction process to
# create various representations.
#
# https://en.wikipedia.org/wiki/Builder_pattern

from abc import ABCMeta, abstractmethod


class Car(object):
    def __init__(self, wheels=4, seats=4, color="Black"):
        self.wheels = wheels
        self.seats = seats
        self.color = color

    def __str__(self):
        return "This is a {0} car with {1} wheels and {2} seats.".format(
            self.color, self.wheels, self.seats
        )


class Builder(metaclass=ABCMeta):
    @abstractmethod
    def set_wheels(self, value):
        pass

    @abstractmethod
    def set_seats(self, value):
        pass

    @abstractmethod
    def set_color(self, value):
        pass

    @abstractmethod
    def get_result(self):
        pass


class CarBuilder(Builder):
    def __init__(self):
        self.car = Car()

    def set_wheels(self, value):
        self.car.wheels = value
        return self

    def set_seats(self, value):
        self.car.seats = value
        return self

    def set_color(self, value):
        self.car.color = value
        return self

    def get_result(self):
        return self.car


class CarBuilderDirector:
    @staticmethod
    def construct():
        return (CarBuilder()
                .set_wheels(8)
                .set_seats(16)
                .set_color("green")
                .get_result())


car = CarBuilderDirector.construct()
print(car)
