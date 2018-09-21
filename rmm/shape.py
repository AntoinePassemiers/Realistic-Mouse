# -*- coding: utf-8 -*-
# shape.py
# author: Antoine Passemiers

import copy
import numpy as np
from abc import abstractmethod, ABCMeta


class Shape(metaclass=ABCMeta):

    @abstractmethod
    def sample(self):
        pass
    
    @abstractmethod
    def area(self):
        pass


class Box(Shape):

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0 = x0, y0
        self.x1, self.y1 = x1, y1
    
    def sample(self):
        x = np.random.randint(self.x1, self.x2)
        y = np.random.randint(self.y1, self.y2)
        return x, y
    
    def area(self):
        return (self.x1 - self.x0) * (self.y1 - self.y0)


class Circle(Shape):

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    def sample(self):
        a = 2. * np.pi * np.random.rand()
        r = self.radius * np.sqrt(np.random.rand())
        x, y = r * np.cos(a), r * np.sin(a)
        x = int(np.round(x))
        y = int(np.round(y))
        return x, y
    
    def area(self):
        return np.pi * self.radius ** 2.


class Triangle(Shape):

    def __init__(self, e1, e2, f1, f2, g1, g2):
        self.E = np.asarray([[e1, e2], [f1, f2], [g1, g2]])
        self.A = np.asarray([[0, 0, 1], [1, 0, 1], [0, 1, 1]])
        self.A_prime = np.linalg.inv(self.A)
        self.P = np.dot(self.A_prime, self.E)        

    def sample(self):
        r1 = np.random.rand()
        r2 = np.random.rand()        
        x1 = np.sqrt(r1) * (1. - r2)
        x2 = np.sqrt(r1) * r2
        y = np.dot([x1, x2, 1], self.P)
        y0 = int(np.round(y[0]))
        y1 = int(np.round(y[1]))
        return y0, y1
    
    def area(self):
        side_a = np.sqrt(np.sum((self.E[0] - self.E[1]) ** 2))
        side_b = np.sqrt(np.sum((self.E[1] - self.E[2]) ** 2))
        side_c = np.sqrt(np.sum((self.E[0] - self.E[2]) ** 2))
        s = float(side_a + side_b + side_c) / 2.
        return np.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))


class Polyline:

    def __init__(self):
        self.vertices = list()
        self.angles = list()
        self.is_clockwise = True
    
    def start(self):
        self.vertices = list()
        self.angles = list()
    
    def stop(self):
        if self.vertices[-1] == self.vertices[0]:
            self.vertices.pop()
            self.angles.pop()
        a = self.vertices[-2]
        b = self.vertices[-1]
        c = self.vertices[0]
        self.add_angle(a, b, c)
        a, b, c = b, c, self.vertices[1]
        self.add_angle(a, b, c)
        self.is_clockwise = (np.sum(self.angles) >= 0)

    def add(self, x, y):
        self.vertices.append([x, y])
        if len(self.vertices) >= 3:
            a = self.vertices[-3]
            b = self.vertices[-2]
            c = self.vertices[-1]
            self.add_angle(a, b, c)   

    def add_angle(self, a, b, c):
        angle = Polyline.compute_angle(a, b, c)
        self.angles.append(angle)
    
    @staticmethod
    def compute_angle(a, b, c):
        a, b, c = np.asarray(a), np.asarray(b), np.asarray(c)
        c, b = c - b, b - a
        dot = b[0] * c[0] + b[1] * c[1]
        det = b[0] * c[1] - b[1] * c[0]
        angle = np.arctan2(det, dot)
        return angle
    
    def remove(self, key):
        del self.vertices[key]
    
    def __getitem__(self, key):
        return self.vertices[key]
    
    def __len__(self):
        return len(self.vertices)


class Polygon(Shape):

    def __init__(self, polyline):
        self.polyline = polyline
        self.triangles = self.ear_clipping()
        self.weights = np.asarray([triangle.area() \
            for triangle in self.triangles])
        self.weights /= self.weights.sum()
    
    def ear_clipping(self):
        """Triangulation based on ear clipping method."""
        polyline = copy.deepcopy(self.polyline)
        triangles = list()
        for i in range(len(polyline) - 2):
            for a in range(len(polyline)):
                b = (a + 1) % len(polyline)
                c = (a + 2) % len(polyline)
                if self.is_convex_at(polyline, a, b, c):
                    e1, e2 = polyline[a][0], polyline[a][1]
                    f1, f2 = polyline[b][0], polyline[b][1]
                    g1, g2 = polyline[c][0], polyline[c][1]
                    polyline.remove(b)
                    triangles.append(Triangle(e1, e2, f1, f2, g1, g2))
                    break
        return triangles
    
    def is_convex_at(self, polyline, a, b, c):
        a = polyline[a]
        b = polyline[b]
        c = polyline[c]
        return (Polyline.compute_angle(a, b, c) >= 0) == polyline.is_clockwise

        return True # TODO
    
    def sample(self):
        triangle = np.random.choice(self.triangles, p=self.weights)
        return triangle.sample()
    
    def area(self):
        return sum([triangle.area() for triangle in self.triangles])


if __name__ == '__main__':
    polyline = Polyline()
    polyline.add(0, 0)
    polyline.add(4, 0)
    polyline.add(4, 2)
    polyline.add(1, 2)
    polyline.add(1, 5)
    polyline.add(0, 5)
    polyline.stop()

    print(polyline.angles)

    polygon = Polygon(polyline)

    print(polygon.area())
    print(polygon.sample())

