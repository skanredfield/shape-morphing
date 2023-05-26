import cv2
from cv2 import Mat
from shape import *


class ShapeRenderer:

    @staticmethod
    def draw_polygon(image: Mat, poly: Polygon, color, thickness):
        for p1, p2 in zip(poly.points, poly.points[1:]):
            print("Drawing a line between ", p1, " and ", p2)
            image = cv2.line(image, p1, p2, color, thickness)
        image = cv2.line(image, poly.points[-1], poly.points[0], color, thickness)
        return image