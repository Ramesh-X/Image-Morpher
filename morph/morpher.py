import numpy as np
from skimage import transform as tf
import matplotlib.pyplot as plt
from PyQt5 import QtCore
from typing import List, NewType

img1_points = np.array([])
img1 = np.array([])
img2 = np.array([])
img2_points = np.array([])
img3_points = np.array([])


def set_data(im1_points: List[QtCore.QPoint], im2_points: List[QtCore.QPoint], im1: np.ndarray, im2: np.ndarray):
    global img1_points, img2_points, img1, img2
    img1_points = generate_points(im1_points, [im1.shape[0], im1.shape[1]])
    img2_points = generate_points(im2_points, [im2.shape[0], im2.shape[1]])
    img1 = im1
    img2 = im2


def generate_points(points: List[QtCore.QPoint], sz: List[int]) -> np.array:
    cords = [[0, 0], [sz[1], sz[0]], [0, sz[0]/2.0], [sz[1], sz[0]/2.0],
             [sz[1]/2.0, 0], [sz[1]/2.0, sz[0]], [0, sz[0]], [sz[1], 0]]
    for point in points:
        cords.append([point.x(), point.y()])
    return np.array(cords)


def pw_aff(alpha: float) -> np.ndarray:
    global img3_points
    img3_points = (1 - alpha) * img1_points + alpha * img2_points
    pw1t3 = tf.PiecewiseAffineTransform()
    pw1t3.estimate(img1_points, img3_points)
    img1t3 = tf.warp(img1, pw1t3.inverse, output_shape=(img1.shape[0], img1.shape[1]))
    pw2t3 = tf.PiecewiseAffineTransform()
    pw2t3.estimate(img2_points, img3_points)
    img2t3 = tf.warp(img2, pw2t3.inverse, output_shape=(img2.shape[0], img2.shape[1]))
    img3 = (1 - alpha) * img1t3 + alpha * img2t3
    return img3
