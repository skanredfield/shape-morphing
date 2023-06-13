from itertools import tee
from math import sqrt
from world_settings import WORLD_SPACE_REFERENCE_WIDTH, WORLD_SPACE_REFERENCE_HEIGHT


class Shape:
    
    @classmethod
    def world_to_local(cls, point, centroid):
        # top left corner of the drawing (world) screen is (0, 0)
        # bottom right is (max_width, max_height)

        # here we simply find the displacement of the point relative to the centroid
        # then we 'rebase' the point to the centroid of (0, 0) in local space
        return (
            (point[0] - centroid[0]),
            -(point[1] - centroid[1])
        )
    
    @classmethod
    def local_to_world(cls, point, centroid):
        # reverse of world_to_local
        return (
            int(point[0] + centroid[0]),
            -int(point[1] - centroid[1])
        )


class Polygon(Shape):
    
    def __init__(self, *points) -> None:
        self.local_points = list(points)
        self.num_points = len(self.local_points)
        self.world_points = None
        self.world_centroid = None

    @classmethod
    def from_world_points(cls, *points):
        world_points = list(points)
        num_points = len(world_points)
        points_sum = sum_points(world_points)
        world_centroid = (points_sum[0] / num_points, points_sum[1] / num_points)
        local_points = [Shape.world_to_local(p, world_centroid) for p in world_points]
        polygon = cls(*local_points)
        polygon.world_centroid = world_centroid
        polygon.world_points = world_points
        return polygon
    
    def update_world_points(self):
        self.world_points = [self.local_to_world(p, self.world_centroid) for p in self.local_points]
    
    def find_closest_local_point(self, ref_point, local_points):
        min_dist = 100000000000.0
        min_point = ref_point
        for p in local_points:
            dist = sqrt((p[0] - ref_point[0]) ** 2 + (p[1] - ref_point[1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                min_point = p

        return min_point
        
    def __str__(self) -> str:
        return "World: {0}\nLocal: {1}".format(str(self.world_points), str(self.local_points))

class MorphedPolygon(Polygon):
    
    def __init__(self, poly1: Polygon, poly2: Polygon, world_centroid) -> None:
        self.poly1 = poly1
        self.poly2 = poly2
        self.resulting_poly = None
        
        # if self.poly1.num_points > self.poly2.num_points:
        #     print("Initial shape is larger")
        #     # initial shape is larger
        #     self.resulting_poly = Polygon(*self.poly1.local_points)
        #     self.initial_poly = self.poly2
        #     self.final_poly = self.poly1
        # else:
        #     print("Final shape is larger")
        #     # final shape is larger
        #     self.resulting_poly = Polygon(*self.poly2.local_points)
        #     self.initial_poly = self.poly1
        #     self.final_poly = self.poly2

        #     closest_point = self.find_closest_local_point(
        #         self.resulting_poly.local_points[-1], 
        #         self.initial_poly.local_points
        #     )
        #     # self.resulting_poly.local_points[-1] = closest_point
        #     # self.initial_poly.local_points[-1] = self.resulting_poly.local_points[-1]
        #     # self.final_poly.local_points[-1] = self.resulting_poly.local_points[-1]
        #     self.initial_poly.local_points[-1] = self.initial_poly.local_points[-2]



        self.initial_poly = subdivide(self.poly1, 20)
        self.final_poly = subdivide(self.poly2, 20)
        self.resulting_poly = Polygon(*self.initial_poly.local_points)

        self.resulting_poly.world_centroid = world_centroid
        self.resulting_poly.update_world_points()

    def morph(self, blend_value01):
        for i in range(0, self.initial_poly.num_points):
            p_i = self.initial_poly.local_points[i]
            p_f = self.final_poly.local_points[i]
            x = p_i[0] * (1.0 - blend_value01) + p_f[0] * (blend_value01)
            y = p_i[1] * (1.0 - blend_value01) + p_f[1] * (blend_value01)
            self.resulting_poly.local_points[i] = (x, y)

            self.resulting_poly.update_world_points()

    
def minmax(numbers):
    min_value = 1e10
    max_value = -1e10

    for n in numbers:
        if n > max_value:
            max_value = n
        if n < min_value:
            min_value = n

    return min_value, max_value

def sum_points(points):
    value_x = 0
    value_y = 0
    for p in points:
        value_x += p[0]
        value_y += p[1]
    
    return (value_x, value_y)

def subdivide(poly: Polygon, new_num_points = 100) -> Polygon:
    num_edges = poly.num_points
    num_points_per_edge = int(new_num_points / num_edges)
    new_local_points = []
    increment = 1.0 / num_points_per_edge
    a, b = tee(poly.local_points)
    next(b, None)

    for p1, p2 in zip(a, b):
        blend_value01 = 0.0
        for _ in range(0, num_points_per_edge):
            x = p1[0] * (1.0 - blend_value01) + p2[0] * (blend_value01)
            y = p1[1] * (1.0 - blend_value01) + p2[1] * (blend_value01)
            blend_value01 += increment
            new_local_points.append((x, y))
    
    # final edge
    blend_value01 = 0.0
    p1 = poly.local_points[-1]
    p2 = poly.local_points[0]
    for _ in range(0, num_points_per_edge):
        x = p1[0] * (1.0 - blend_value01) + p2[0] * (blend_value01)
        y = p1[1] * (1.0 - blend_value01) + p2[1] * (blend_value01)
        blend_value01 += increment
        new_local_points.append((x, y))
    
    return Polygon(*new_local_points)
        