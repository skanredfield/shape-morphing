from world_settings import WORLD_SPACE_REFERENCE_WIDTH, WORLD_SPACE_REFERENCE_HEIGHT


class Shape:
    
    def world_to_local(self, point, centroid):
        print('Centroid: ', centroid)
        return (
            (point[0] - centroid[0]),
            (point[1] - centroid[1])
        )


class Polygon(Shape):
    
    def __init__(self, *points) -> None:
        self.points = list(points)
        num_points = len(self.points)
        points_sum = sum_points(self.points)
        centroid = (points_sum[0] / num_points, points_sum[1] / num_points)
        self.local_points = [self.world_to_local(p, centroid) for p in self.points]

    def __str__(self) -> str:
        return str(self.local_points)

class MorphedPolygon():
    
    def __init__(self, poly1: Polygon, poly2: Polygon) -> None:
        self.poly1 = poly1
        self.poly2 = poly2
        
        self.num_vetices = max(len(poly1.points), len(poly2.points))

    def morph(self, blend_value01):
        points = []
        for p1 in self.poly1.points:
            for p2 in self.poly2.points:
                # TODO: first need to move to local space
                pass
    

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