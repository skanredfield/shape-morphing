import cv2
import numpy as np
from shape import Polygon

"""
Draw shapes here.
"""

img = None
points = []
window_name = None

def place_point(x, y):
    global img, window_name, points

    curr_point = (x, y)
    points.append(curr_point)

    # Uncomment to show coordinates
    # --------------------------------
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # coords_text = f'({x},{y})'
    # cv2.putText(img, coords_text, (x+10, y+10), font, 0.5, (255, 0, 0), 2)

    cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

    # add a line
    if len(points) > 1:
        prev_point = points[len(points)-2]
        cv2.line(img, prev_point, curr_point, (0, 0, 255), 3)

    cv2.imshow(window_name, img)

def mend_points_return_shape(window_width, window_height):
    global points
    # make sure that the first and last points are the same
    points.pop()
    # normalize the points so they are independent of the window size
    return Polygon.from_world_points(*[(x / window_width, y / window_height) for (x, y) in points])

def draw_shape(win_name, window_width, window_height):
    global img, window_name, points
    points.clear()
    window_name = win_name
    img = np.zeros((window_height, window_width, 3), np.uint8)
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_width, window_height)
    cv2.setMouseCallback(window_name, onClickEvent)
    cv2.imshow(window_name, img)

    try:
        while cv2.getWindowProperty(window_name, 0) >= 0:
            k = cv2.waitKey(1) & 0xFF
            if k == 13:
                # enter key -- means we submit the image
                break
            if k == 27:
                # escape key -- means we dismiss the image
                points.clear()
                break
    except:
        print("No window ", window_name, " could be found")

    cv2.destroyAllWindows()
    if len(points) > 0:
        return mend_points_return_shape(window_width, window_height)
    return None


def onClickEvent(event, x, y, flags, params):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        place_point(x, y)
    else:
        pass

