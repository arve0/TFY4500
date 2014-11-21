#!/usr/bin/env python
# encoding: utf-8
"Generate pngs of tifs in current or specified directory."


from __future__ import division
import os, sys, glob, png
from scipy.ndimage import imread
from scipy.misc import imresize
import numpy as np

def equalization(img):
    "Contrast enhancement through histogram equalization."
    # exclude values <= 2
    threshold = 2
    hist = np.bincount(img[img>threshold].flatten())
    cdf = (hist / img[img>threshold].size).cumsum()
    equal_img = np.copy(img) # copy to get values below threshold
    for level, h in enumerate(hist):
        if h == 0: continue # short cut
        mask = (img == level)
        equal_img[mask] = cdf[level] * 255
    return equal_img

def pngwrite(filename, data):
    """
    Write data to png file.

    :parameter string filename: String with filename
    :parameter ndarray data: Numpy array with data
    
    :return: None
    """
    newsize = (int(data.shape[0]/10), int(data.shape[1]/10))
    data = imresize(data, newsize)
    data = equalization(data)
    f = open(filename, 'wb') # write binary
    w = png.Writer(greyscale=True, width=data.shape[1], height=data.shape[0])
    w.write(f, data)
    f.close()


def main():
    """
    Run when script executed.
    """

    if len(sys.argv) == 2:
        path = os.path.realpath(sys.argv[1])
        os.chdir(path)
    else:
        path = os.getcwd()
    print('Finding tif files in directory: ' + path)
    files = glob.glob('*.tif')

    for n, f in enumerate(files):
        pngname = 'png/' + f.split('.tif')[0] + '.png'
        print('saving to ' + pngname)
        pngwrite(pngname, imread(f))


if __name__ == '__main__':
    main()
