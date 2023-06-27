# Simple polygonal shape morphing

This repo contains a python program using OpenCV that let's you define two shapes and then animate the transition between the them.

## Instructions

1. Left click to place points of the shape. Last and first points will form the final edge.
2. Press Enter to continue.
3. Once the main window with the two shapes and the morphed shape is shown, you can either use the trackbar at the top to control blending between the shapes, or press Space to toggle the animation loop.

Additionally, several useful flags can be changed in the morphing_simple_shape.py file.

- IS_DRAWING_SHAPES defines whether the morphed shape is rendered with dots or lines
- IS_RENDERING_LINES_DURING_ANIMATION same, but for animation
- SUBDIVISION_LEVEL is the multiple of the number of common subdivisions between the shapes (higher value will make the animation smoother, but might hit the performance)
- USE_TRANSFORMATION_MAP tells the program whether the points should be transformed according to their proximitiy or just index-wise
