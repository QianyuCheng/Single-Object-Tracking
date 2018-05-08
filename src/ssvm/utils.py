"""Useful functions."""

import os
import pickle
import matplotlib.pyplot as plt
import numpy as np


def load_dataset(data_path, mode='TLP'):

    img_path = data_path + "/img/"
    truth_path = data_path + "/groundtruth_rect.txt"

    if mode == 'TLP':
        truths = []
        with open(truth_path, "rt") as f:
            for line in f.readlines():
                truths += [np.array(line.strip().split(","), dtype=int)[1:-1]]
    else:
        truths = []
        with open(truth_path, "rt") as f:
            for line in f.readlines():
                truths += [np.array(line.strip().split(","), dtype=int)]

    files = os.listdir(img_path)
    files.sort()
    frames = []
    for f in files:
        frames += [plt.imread(img_path + f)]

    return (frames, truths)


def draw_rect_on_frame(frame, rect, linewidth=2, color=[255, 255, 255]):
    """Draw rectangle on an image."""
    (x, y, w, h) = np.array(rect).astype(int)
    color = np.array(color, dtype=np.uint8)
    frame[y-linewidth:y+h, x-linewidth:x, :] = color
    frame[y-linewidth:y+h, x+w-linewidth:x+w, :] = color
    frame[y-linewidth:y, x:x+w, :] = color
    frame[y+h-linewidth:y+h, x:x+w, :] = color
    return frame


def overlap_rate(a, b):
    (x0, y0, w0, h0) = a
    (x, y, w, h) = b
    (x0_, y0_, x_, y_) = (x0+w0, y0+h0, x+w, y+h)
    (left, top) = (np.maximum(x, x0), np.maximum(y, y0))
    (right, bottom) = (np.minimum(x_, x0_), np.minimum(y_, y0_))
    intersect = np.maximum(bottom - top, 0) * np.maximum(right - left, 0)
    union = w * h + w0 * h0 - intersect
    return intersect / union

def accuracy(a, b):
    assert len(a) == len(b)
    score = 0
    for i in range(1, len(a)):
        dax = a[i][0] - a[i-1][0]
        day = a[i][1] - a[i-1][1]
        dbx = b[i][0] - b[i-1][0]
        dby = b[i][1] - b[i-1][1]
        dd = (dax - dbx) ** 2 + (day - dby) ** 2
        ovr = overlap_rate(a[i], b[i])
        if dd == 0:
            score += ovr
        else:
            ovr / dd
    return score
