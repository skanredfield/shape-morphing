import cv2
from cv2 import Mat
from shape import *


class ShapeRenderer:

    @staticmethod
    def draw_polygon(image: Mat, poly: Polygon, color, thickness):
        for p1, p2 in zip(poly.world_points, poly.world_points[1:]):
            # print("Drawing a line between ", p1, " and ", p2)
            image = cv2.line(image, p1, p2, color, thickness)
        image = cv2.line(image, poly.world_points[-1], poly.world_points[0], color, thickness)
        # print("Drawing a line between ", poly.world_points[-1], " and ", poly.world_points[0],)
        return image
    
    @staticmethod
    def draw_points(image: Mat, poly: Polygon, color):
        for p in poly.world_points:
            image = cv2.circle(image, p, 1, color)
        return image