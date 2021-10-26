#!/usr/bin/env python3
from node import Node

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Quadtree:
    """
    Quadtree defined by its root and # of levels in it
    Root at level 0
    """
    def __init__(self, image, nlevels):
        self.image = image
        self.rows, self.cols, _ = self.image.shape
        self.root = Node(0, 0, self.rows, self.cols, self.image, 0)
        self.nlevels = nlevels

        # bfs traversal to construct tree by level going downward
        self.fifo = []
        self.ramify()

    def ramify(self):
        """
        Create quadtree by ramification (i.e. cut image into four quadrants)
        Based on BFS traversal to build level i before level i+1 (using a fifo)
        param parent Parent node (modified in place)
        """
        self.fifo.insert(0, self.root)

        while len(self.fifo) > 0:
            parent = self.fifo.pop()

            # stop condition
            if parent.level == self.nlevels:
                break

            # nrows and ncols can be odd
            nrows_child0 = parent.nrows // 2
            nrows_child1 = parent.nrows - nrows_child0
            ncols_child0 = parent.ncols // 2
            ncols_child1 = parent.ncols - ncols_child0
            logger.info('({}, {}, {}, {})'.format(nrows_child0, nrows_child1, ncols_child0, ncols_child1))

            # quadrants subsets of size = 0
            if nrows_child0 == 0 or nrows_child1 == 0 or ncols_child0 == 0 or ncols_child1 == 0:
                break

            # child at north-west
            row = parent.row
            col = parent.col
            nrows = nrows_child0
            ncols = ncols_child0
            image = self.image[row:row+nrows, col:col+ncols]
            child00 = Node(row, col, nrows, ncols, image, parent.level + 1)

            # child at north-east
            row = parent.row
            col = parent.col + ncols_child0
            nrows = nrows_child0
            ncols = ncols_child1
            image = self.image[row:row+nrows, col:col+ncols]
            child01 = Node(row, col, nrows, ncols, image, parent.level + 1)

            # child at south-west
            row = parent.row + nrows_child0
            col = parent.col
            nrows = nrows_child1
            ncols = ncols_child0
            image = self.image[row:row+nrows, col:col+ncols]
            child10 = Node(row, col, nrows, ncols, image, parent.level + 1)

            # child at south-east
            row = parent.row + nrows_child0
            col = parent.col + ncols_child0
            nrows = nrows_child1
            ncols = ncols_child1
            image = self.image[row:row+nrows, col:col+ncols]
            child11 = Node(row, col, nrows, ncols, image, parent.level + 1)

            # push into fifo four children to further subdivide them in next iterations
            parent.children = [child00, child01, child10, child11]
            self.fifo.insert(0, child00)
            self.fifo.insert(0, child01)
            self.fifo.insert(0, child10)
            self.fifo.insert(0, child11)

    def traverse(self, node, level, nodes):
        """
        Recursive DFS traversal to find quadtree nodes at given level
        return nodes List of nodes at given level
        # of nodes @ level l = 4**l
        """
        if level > self.nlevels:
            logger.error('Traverse: level cannot be bigger than nlevels')
            return

        if node.level == level:
            nodes.append(node)
            return

        for child in node.children:
            self.traverse(child, level, nodes)

    def concat(self, node, level):
        """
        Recursive concatenation to reconstruct initial image
        @param level Requested level
        """
        if level > self.nlevels:
            logger.error('Concat: level cannot be bigger than nlevels')
            return

        # stop condition
        children = node.children
        if node.level == level or len(children) == 0:
            return node.image

        return [
            [concat(children[0], level), concat(children[1], level)],
            [concat(children[2], level), concat(children[3], level)],
        ]
