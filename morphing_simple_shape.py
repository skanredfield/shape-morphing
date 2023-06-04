import cv2
import numpy as np
from cv2 import Mat
from shape import *
from shape_renderer import ShapeRenderer
from world_settings import set_world_size


WORLD_WIDTH = 500
WORLD_HEIGHT = 500

base_img: Mat = None
drawing_img: Mat = None

morphed_shape: MorphedPolygon = None

def show_simple_unfilled_shapes_morphing(window_name, window_width, window_height):
    global base_img, drawing_img

    cv2.namedWindow(window_name)
    cv2.createTrackbar("Blend", window_name, 0, 100, onBlendValueChanged)

    drawing_img = np.zeros((window_height, window_width, 3), np.uint8)

    shape1 = Polygon.from_world_points((50, 50), (150, 50), (150, 150), (50, 150))
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, shape1, (0, 255, 0), 2)
    print('Shape 1:\n', shape1)

    shape2 = Polygon.from_world_points((300, 80), (370, 40), (440, 80), (410, 160), (330, 160))
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, shape2, (255, 0, 0), 2)
    print('Shape 2:\n', shape2)

    base_img = drawing_img.copy()

    global morphed_shape
    morphed_shape = MorphedPolygon(shape1, shape2, (250, 350))
    morphed_shape.morph(0)
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, morphed_shape.resulting_poly, (0, 0, 255), 2)
    print('Morphed shape:\n', morphed_shape.resulting_poly)

    
    while cv2.getWindowProperty(window_name, 0) >= 0:
        cv2.imshow(window_name, drawing_img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

def onBlendValueChanged(val):
    global base_img, drawing_img, morphed_shape
    value01 = val / 100.0
    drawing_img = base_img.copy()

    morphed_shape.morph(value01)
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, morphed_shape.resulting_poly, (0, 0, 255), 2)

set_world_size(WORLD_WIDTH, WORLD_HEIGHT)
show_simple_unfilled_shapes_morphing("Simple Shapes", WORLD_WIDTH, WORLD_HEIGHT)