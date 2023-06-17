import cv2
import numpy as np
from cv2 import Mat
from shape import *
from shape_renderer import ShapeRenderer
from shape_input import draw_shape
from world_settings import set_world_size
from math import sin


IS_DRAWING_SHAPES = True
IS_RENDERING_LINES_DURING_ANIMATION = False

WORLD_WIDTH = 800
WORLD_HEIGHT = 600

NUM_SUBDIVISIONS = 50

base_img: Mat = None
drawing_img: Mat = None

morphed_shape: MorphedPolygon = None

is_anim_loop_running = False
anim_val = 0

def show_simple_unfilled_shapes_morphing(window_name, window_width, window_height):
    global base_img, drawing_img

    drawing_img = np.zeros((window_height, window_width, 3), np.uint8)

    if not IS_DRAWING_SHAPES:
        shape1 = Polygon.from_world_points((150, 50), (250, 50), (250, 150), (150, 150))

        shape2 = Polygon.from_world_points((500, 80), (570, 40), (640, 80), (610, 160), (530, 160))
    else:
        shape1 = draw_shape("Initial Shape", window_width, window_height)
        shape1.world_centroid = (150, 100)
        shape1.renormalize(WORLD_WIDTH * 0.3, WORLD_HEIGHT * 0.3)

        shape2 = draw_shape("Final Shape", window_width, window_height)
        shape2.world_centroid = (600, 100)
        shape2.renormalize(WORLD_WIDTH * 0.3, WORLD_HEIGHT * 0.3)
    
    cv2.namedWindow(window_name)
    cv2.createTrackbar("Blend", window_name, 0, 100, onBlendValueChanged)
    # cv2.createButton("Play", onPlayButtonPressed, None, cv2.QT_PUSH_BUTTON, 1)

    drawing_img = ShapeRenderer.draw_polygon(drawing_img, shape1, (0, 255, 0), 2)
    print('Shape 1:\n', shape1)
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, shape2, (255, 0, 0), 2)
    print('Shape 2:\n', shape2)

    
    # subdivided_poly = subdivide(shape1, 100)
    # subdivided_poly.world_centroid = (100, 300)
    # subdivided_poly.update_world_points()
    # drawing_img = ShapeRenderer.draw_points(drawing_img, subdivided_poly, (255, 0, 255))


    base_img = drawing_img.copy()

    global morphed_shape
    shape1.renormalize(2, 2)
    shape2.renormalize(2, 2)
    morphed_shape = MorphedPolygon(shape1, shape2, (400, 400), NUM_SUBDIVISIONS)
    morphed_shape.morph(0)
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, morphed_shape.resulting_poly, (0, 0, 255), 2)
    print('Morphed shape:\n', morphed_shape.resulting_poly)

    global is_anim_loop_running, anim_val
    while cv2.getWindowProperty(window_name, 0) >= 0:
        cv2.imshow(window_name, drawing_img)
        if is_anim_loop_running:
            update_anim_loop()
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        if key == 32:
            is_anim_loop_running = not is_anim_loop_running
            anim_val = 0


def update_anim_loop():
    global base_img, drawing_img, morphed_shape, anim_val
    
    value01 = sin(anim_val / 100.0 * 2) * 0.5 + 0.5
    anim_val += 1

    drawing_img = base_img.copy()

    morphed_shape.morph(value01)
    if IS_RENDERING_LINES_DURING_ANIMATION:
        drawing_img = ShapeRenderer.draw_polygon(drawing_img, morphed_shape.resulting_poly, (0, 0, 255), 2)
    else:
        drawing_img = ShapeRenderer.draw_points(drawing_img, morphed_shape.resulting_poly, (255, 0, 255))

def onBlendValueChanged(val):
    global base_img, drawing_img, morphed_shape
    value01 = val / 100.0
    drawing_img = base_img.copy()

    morphed_shape.morph(value01)
    drawing_img = ShapeRenderer.draw_polygon(drawing_img, morphed_shape.resulting_poly, (0, 0, 255), 2)

def onPlayButtonPressed(*args):
    pass

set_world_size(WORLD_WIDTH, WORLD_HEIGHT)
show_simple_unfilled_shapes_morphing("Simple Shapes", WORLD_WIDTH, WORLD_HEIGHT)
