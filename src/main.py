#!/usr/bin/env python3
"""
Pixelate image with Quadtree (no compression)
inspired by: https://medium.com/analytics-vidhya/transform-an-image-into-a-quadtree-39b3aa6e019a
TODO:
- Stop image subdivision in quadtree using threshold (RMSE relative to avg.)
- Use quadtree to compress image.
"""
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from numpy.core.shape_base import block
import math
import operator
import argparse

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from quadtree import Quadtree


if __name__ == '__main__':
    # parse cli arguments (nargs='?' => optional parameter)
    parser = argparse.ArgumentParser()
    parser.add_argument('path_image', help='Path to input image')
    parser.add_argument('n_levels', nargs='?', type=int, default=7, help='Number of levels in the quadtree')
    parser.add_argument('level', nargs='?', type=int, default=6, help='Level of image to show')
    args = parser.parse_args()

    # quadtree from image
    # img_in = mpimg.imread('assets/synthetic.png')
    img_in = mpimg.imread(args.path_image)
    logger.info('Input image: {}'.format(img_in.shape))
    quadtree = Quadtree(img_in, nlevels=args.n_levels)

    # dfs traversal of quadtree till given level
    nodes_level = []
    quadtree.traverse(quadtree.root, level=args.level, nodes=nodes_level)
    n_nodes = len(nodes_level)
    logger.info('Nodes @level: {}'.format(n_nodes))

    # set pixel in output image to average color from quadtree
    img_out = np.zeros(img_in.shape)
    for node in nodes_level:
        get_attrs = operator.attrgetter('row', 'col', 'nrows', 'ncols')
        row, col, nrows, ncols =  get_attrs(node)
        img_out[row:row+nrows, col:col+ncols] = node.image

    # important to convert to ints (otherwise floats must be in [0, 1], not case with avg.)
    img_out = img_out.astype(int)

    # show input & output images
    figs, ax = plt.subplots(1, 2)
    ax[0].imshow(img_in)
    ax[1].imshow(img_out)
    plt.show()
