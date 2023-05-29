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

def show_simple_unfilled_shapes_morphing(window_name, window_width, window_height):
    global base_img, drawing_img

    cv2.namedWindow(window_name)
    cv2.createTrackbar("Blend", window_name, 0, 100, onBlendValueChanged)

    drawing_img = np.zeros((window_height, window_width, 3), np.uint8)

    shape1 = Polygon((50, 50), (150, 50), (150, 150), (50, 150))
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, shape1, (0, 255, 0), 2)
    print('Shape1: ', shape1)

    shape2 = Polygon((300, 80), (370, 40), (440, 80), (410, 160), (330, 160))
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, shape2, (255, 0, 0), 2)
    print('Shape2: ', shape2)

    base_img = drawing_img.copy()

    
    while cv2.getWindowProperty(window_name, 0) >= 0:
        cv2.imshow(window_name, drawing_img)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

def onBlendValueChanged(val):
    global base_img, drawing_img
    value01 = val / 100.0
    drawing_img = base_img.copy()
    if val != 0:
        drawing_img = cv2.line(drawing_img, (250, 400), (250 + val, 400), (0, 0, 255), 2)

set_world_size(WORLD_WIDTH, WORLD_HEIGHT)
show_simple_unfilled_shapes_morphing("Simple Shapes", WORLD_WIDTH, WORLD_HEIGHT)