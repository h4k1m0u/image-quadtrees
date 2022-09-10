#!/usr/bin/env python3
import image_operations

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Node:
    """
    Defines offsets & size of subimage (image not stored)
    Level saved to retrieve all nodes at a certain level
    @param row, col Offsets in row/col directions
    @param row, col # of rows/cols in subimage
    """
    def __init__(self, row, col, nrows, ncols, image, level):
        self.row = row
        self.col = col
        self.nrows = nrows
        self.ncols = ncols
        self.children = []
        self.level = level
        self.image = image_operations.average(image)

        logger.info('level: {0}, row: {1}, col: {2}, nrows: {3}, ncols: {4}'.format(level, row, col, nrows, ncols))

    def __str__(self):
        """
        Called when printing a Node instance
        """
        return f'Node level={self.level} size={self.nrows}x{self.ncols} offset={self.row}:{self.col}'
