class Shape:
    pass

class Polygon(Shape):
    
    def __init__(self, *points) -> None:
        self.points = list(points)

    def __str__(self) -> str:
        return str(self.points)

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
    