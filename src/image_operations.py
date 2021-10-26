#!/usr/bin/env python3
import numpy as np


def split(image):
    """
    Split given image into four quadrants
    """
    image0, image1 = np.array_split(image, 2)
    image00, image01 = np.array_split(image0, 2, axis=1)
    image10, image11 = np.array_split(image1, 2, axis=1)

    return [image00, image01, image10, image11]

def join(image00, image01, image10, image11):
    """
    Join together four quadrants into a single image
    """
    image0 = np.concatenate([image00, image01], axis=1)
    image1 = np.concatenate([image10, image11], axis=1)
    image = np.concatenate([image0, image1])

    return image

def average(image):
    """
    Average color for each quadrant
    """
    return np.mean(image.reshape([-1, 4]), axis=0)
