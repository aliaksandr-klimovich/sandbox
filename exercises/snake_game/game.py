import abc
import random
from collections import namedtuple
from typing import List, Set, Dict, Union

import pygame

CELL_SIZE = 32
ROWS = 16
COLS = 16

SCREEN_SIZE = WIDTH, HEIGHT = CELL_SIZE * COLS, CELL_SIZE * ROWS

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

cell_img = pygame.image.load('img/stone.png')
snake_head = pygame.image.load('img/blue_grass.png')
snake_body = pygame.image.load('img/grass.png')
food_img = pygame.image.load('img/orange_grass.png')

Point = namedtuple('Point', 'x, y')


class ExPoint:
    __slots__ = ('x', 'y')

    def __init__(self, x_or_point: Union[int, Point], y=None):
        if isinstance(x_or_point, Point):
            self.x = x_or_point.x
            self.y = x_or_point.y
        else:
            self.x = x_or_point
            self.y = y

    def to_point(self):
        return Point(self.x, self.y)


class SurfaceObject(abc.ABC):
    points: List[Point]

    @abc.abstractmethod
    def get_img(self, point: Point):
        pass


class Snake(SurfaceObject):
    def __init__(self, start_points=(Point(2, 0), Point(1, 0), Point(0, 0))):
        self.points = list(start_points)

    @property
    def head(self) -> Point:
        return self.points[0]

    def move_to(self, point: Point, eat=False) -> bool:

        if (0 <= point.x < COLS and 0 <= point.y < ROWS and
                point not in self.points and
                point in (Point(self.points[0].x + 0, self.points[0].y + 1),
                          Point(self.points[0].x + 1, self.points[0].y + 0),
                          Point(self.points[0].x - 0, self.points[0].y - 1),
                          Point(self.points[0].x - 1, self.points[0].y - 0))):

            self.points.insert(0, point)
            if eat is False:
                self.points.pop()

            return True
        return False

    def get_img(self, point: Point):
        if point in self.points:
            if point == self.head:
                return snake_head
            else:
                return snake_body

    def eat(self, point: Point, obj: SurfaceObject):
        self.move_to(point, eat=True)
        try:
            obj.points.remove(point)
        except ValueError:
            pass


snake = Snake()


class Food(SurfaceObject):
    def __init__(self):
        self.points = [Point(random.randrange(0, COLS), random.randrange(1, ROWS))]

    def get_img(self, point: Point):
        if point in self.points:
            return food_img

    def generate(self, free_points: List[Point]):
        if free_points:
            point = random.choice(free_points)
            self.points.append(point)


food = Food()


class Surface:
    def __init__(self, cols=COLS, rows=ROWS, cell_size=CELL_SIZE, objects: List[SurfaceObject] = None):
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.objects = objects or []

    def _get_objects_point(self) -> Dict[Point, SurfaceObject]:
        buf = {}
        for obj in self.objects:
            for point in obj.points:
                buf[point] = obj
        return buf

    def redraw(self):
        screen.fill((0, 0, 0))

        buf = self._get_objects_point()

        for x in range(self.rows):
            for y in range(self.cols):

                point = Point(x, y)
                if point in buf:
                    img = buf[point].get_img(point)
                    screen.blit(img, (self.cell_size * x, self.cell_size * y))
                else:
                    screen.blit(cell_img, (self.cell_size * x, self.cell_size * y))

        pygame.display.flip()

    def get_used_point(self) -> Set[Point]:
        used_points = set()
        for obj in self.objects:
            for point in obj.points:
                used_points.add(point)
        return used_points

    def get_free_points(self) -> Set[Point]:
        used_points = self.get_used_point()
        free_points = set()
        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) not in used_points:
                    free_points.add(Point(x, y))

        return free_points


surface = Surface(objects=[snake, food])
for i in range(20):
    food.generate(list(surface.get_free_points()))
surface.redraw()


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    do_redraw = True

    destination = ExPoint(snake.head)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        destination.x += 1
    elif keys[pygame.K_LEFT]:
        destination.x -= 1
    elif keys[pygame.K_UP]:
        destination.y -= 1
    elif keys[pygame.K_DOWN]:
        destination.y += 1
    else:
        do_redraw = False

    destination_point = destination.to_point()
    if destination_point in food.points:
        snake.eat(destination_point, food)
        food.generate(list(surface.get_free_points()))
    else:
        snake.move_to(destination_point)

    if do_redraw:
        surface.redraw()

    pygame.time.wait(10)
