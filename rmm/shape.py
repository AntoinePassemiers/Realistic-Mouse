# -*- coding: utf-8 -*-
# shape.py
# author: Antoine Passemiers

import copy
import numpy as np
from abc import abstractmethod, ABCMeta


class Shape(metaclass=ABCMeta):

    def __iadd__(self, point):
        dx, dy = point
        coords = self.get_coords()
        new_coords = list()
        for x, y in coords:
            new_coords.append((x + dx, y + dy))
        self.set_coords(new_coords)
        return self

    def __isub__(self, point):
        dx, dy = point
        coords = self.get_coords()
        new_coords = list()
        for x, y in coords:
            new_coords.append((x - dx, y - dy))
        self.set_coords(new_coords)
        return self

    @abstractmethod
    def sample(self):
        pass
    
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def contains(self, x, y):
        pass
    
    @abstractmethod
    def get_coords(self):
        pass
    
    @abstractmethod
    def set_coords(self, points):
        pass


class Point(Shape):

    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def sample(self):
        return self.x, self.y
    
    def area(self):
        return 0 # TODO: or 1?
    
    def contains(self, x, y):
        return (self.x == x) and (self.y == y)
    
    def get_coords(self):
        return [(self.x, self.y)]
    
    def set_coords(self, points):
        point = points[0]
        self.x, self.y = point[0], point[1]


class Box(Shape):

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0 = x0, y0
        self.x1, self.y1 = x1, y1
    
    def sample(self):
        x = np.random.randint(self.x0, self.x1)
        y = np.random.randint(self.y0, self.y1)
        return x, y
    
    def area(self):
        return (self.x1 - self.x0) * (self.y1 - self.y0)
    
    def contains(self, x, y):
        return (self.x0 <= x <= self.x1) and (self.y0 <= y <= self.y1)
    
    def get_coords(self):
        return [(self.x0, self.y0), (self.x1, self.y1)]
    
    def set_coords(self, points):
        p0, p1 = points
        self.x0, self.y0, self.x1, self.y1 = p0[0], p0[1], p1[0], p1[1]


class Circle(Shape):

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    def sample(self):
        a = 2. * np.pi * np.random.rand()
        r = self.radius * np.sqrt(np.random.rand())
        x = r * np.cos(a) + self.x
        y = r * np.sin(a) + self.y
        x = int(np.round(x))
        y = int(np.round(y))
        return x, y
    
    def area(self):
        return np.pi * self.radius ** 2.
    
    def contains(self, x, y):
        distance = np.sqrt((x - self.x) ** 2. + (y - self.y) ** 2.)
        return distance <= self.radius

    def get_coords(self):
        return [(self.x, self.y)]
    
    def set_coords(self, points):
        center = points[0]
        self.x, self.y = center[0], center[1]


class Triangle(Shape):

    A = np.asarray([[0, 0, 1], [1, 0, 1], [0, 1, 1]])
    A_PRIME = np.linalg.inv(A)

    def __init__(self, e, f, g):
        self.E = np.asarray([e, f, g])
        self.P = None
    
    def cross_product_z_coord(self, a, b):
        return a[0] * b[1] - a[1] * b[0]

    def on_same_side(self, a, b, l1, l2):
        z1 = self.cross_product_z_coord(l2-l1, a-l1)
        z2 = self.cross_product_z_coord(l2-l1, b-l1)
        if z1 == 0 or z2 == 0:
            return True
        else:
            return np.positive(z1) == np.positive(z2)
    
    def contains(self, x, y):
        p = (x, y)
        e, f, g = self.E[0], self.E[1], self.E[2]
        if not self.on_same_side(p, e, f, g):
            return False
        elif not self.on_same_side(p, f, e, g):
            return False
        elif not self.on_same_side(p, g, e, f):
            return False
        else:
            return True

    def sample(self):
        if self.P is None:
            self.P = np.dot(Triangle.A_PRIME, self.E)
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

    def get_coords(self):
        return [self.E[0], self.E[1], self.E[2]]
    
    def set_coords(self, points):
        a, b, c = points
        self.E[0][0], self.E[0][1] = a[0], a[1]
        self.E[1][0], self.E[1][1] = b[0], b[1]
        self.E[2][0], self.E[2][1] = c[0], c[1]


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
        self.vertices.append((x, y))
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
    
    def remove(self, point):
        key = self.vertices.index(point)
        del self.vertices[key]
        del self.angles[(key + 1) % len(self.angles)]
    
    def get_adjacent_vertices(self, b):
        i = self.vertices.index(b)
        a = self.__getitem__(i-1)
        c = self.__getitem__(i+1)
        return a, c
    
    def __getitem__(self, key):
        if type(key) == int:
            key = key % self.__len__()
        return self.vertices[key]
    
    def __len__(self):
        return len(self.vertices)


class Polygon(Shape):

    def __init__(self, polyline):
        self.triangles = self.ear_clipping(polyline)
        self.weights = np.asarray([triangle.area() for triangle in self.triangles])
        self.weights /= self.weights.sum()
    
    def ear_clipping(self, polyline):
        """Triangulation based on ear clipping method.

        References:
            https://www.geometrictools.com/Documentation/TriangulationByEarClipping.pdf
        """
        polyline = copy.deepcopy(polyline)

        convex_vertices = set()
        reflex_vertices = set()
        ear_tips = set()
        for p in range(len(polyline)):
            b = polyline[p]
            if self.is_convex_vertex(polyline, b):
                convex_vertices.add(b)
                if self.is_ear_tip(polyline, b):
                    ear_tips.add(b)
            else:
                reflex_vertices.add(b)
        
        triangles = list()
        n_triangles = len(polyline) - 2
        for i in range(n_triangles):
            if len(ear_tips) == 0:
                break
            ear_id = int(np.random.randint(0, len(ear_tips)))
            b = list(ear_tips)[ear_id]
            a, c = polyline.get_adjacent_vertices(b)
            triangles.append(Triangle(a, b, c))
            polyline.remove(b)
            ear_tips.remove(b)
            convex_vertices.remove(b)
            for p in [a, c]:
                if (p in ear_tips) and not self.is_ear_tip(polyline, p):
                    ear_tips.remove(p)
                elif (p in reflex_vertices) and self.is_convex_vertex(polyline, p):
                    reflex_vertices.remove(p)
                    convex_vertices.add(p)
                if (p in convex_vertices) and self.is_ear_tip(polyline, p):
                    ear_tips.add(p)
        return triangles
    
    def is_convex_vertex(self, polyline, b):
        a, c = polyline.get_adjacent_vertices(b)
        return (Polyline.compute_angle(a, b, c) >= 0) == polyline.is_clockwise
    
    def is_ear_tip(self, polyline, b):
        a, c = polyline.get_adjacent_vertices(b)
        triangle = Triangle(a, b, c)
        ear_tip = True
        for p in polyline.vertices:
            if p not in [a, b, c]:
                if triangle.contains(*p):
                    ear_tip = False
                    break
        return ear_tip
    
    def sample(self):
        triangle = np.random.choice(self.triangles, p=self.weights)
        return triangle.sample()
    
    def area(self):
        return sum([triangle.area() for triangle in self.triangles])

    def contains(self, x, y):
        contained = False
        for triangle in self.triangles:
            if triangle.contains(x, y):
                contained = True
                break
        return contained

    def get_coords(self):
        coords = list()
        for triangle in self.triangles:
            coords += triangle.get_coords()
        return coords
    
    def set_coords(self, points):
        for i, triangle in zip(range(0, len(points), 3), self.triangles):
            triangle.set_coords(points[i:i+3])
