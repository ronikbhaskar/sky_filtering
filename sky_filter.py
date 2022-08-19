"""
The purpose of this script is to filter out the sky in images of Monarch Butterflies.
The sky will be turned white, including most non-cumulonimbus clouds.

References:
https://towardsdatascience.com/image-processing-with-python-color-isolation-for-beginners-3b472293335b
https://scikit-image.org

Author: Ronik
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imshow, imread, imsave
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
import argparse

OUT_DIR = "filtered_images"

def splitter(image, do_hsv = False):
    """
    splitter - visualization tool, splits image into rgb or hsv values, displays with matplotlib
    
    image: np.ndarray - 3D tensor representing image
    
    do_hsv: bool = False - optional, defaults to rgb
    
    Returns: None
    """

    if do_hsv:
        image = rgb2hsv(image)
        titles = ["Hue", "Saturation", "Value"]
        cmaps = ['hsv','Greys','gray']
    else:
        titles = cmaps = ['Reds','Greens','Blues']

    fig, ax = plt.subplots(1, 3, figsize=(15,5), sharey=True)
    imgs = list(range(3))
    for i in range(3):
        imgs[i] = ax[i].imshow(image[:,:,i], cmap = cmaps[i])
        ax[i].set_title(titles[i], fontsize = 15)
        fig.colorbar(imgs[i] ,ax=ax[i])
    plt.show()

def make_sky_filter(image):
    """
    make_sky_filter - filters just the pixels representing the sky
    
    image: np.ndarray - 3D tensor representing image
    
    Returns: filtered image : np.ndarray
    """
    
    image_hsv = rgb2hsv(image)
    
    # Sky Filter, exact values can be modified as necessary
    lower_mask = image_hsv[:,:,0] > 0.45
    upper_mask = image_hsv[:,:,0] < 0.75
    lower_saturation_mask = image_hsv[:,:,1] > 0.20 # between 20 and 40 are good places to test first
    upper_saturation_mask = image_hsv[:,:,1] < 0.90
    value_mask = image_hsv[:,:,2] > 0.25 # doesn't change much, can be removed if so desired
    mask = lower_mask * upper_mask * lower_saturation_mask * upper_saturation_mask * value_mask
    
    sky_filter = np.dstack((image[:,:,0] * mask,
                            image[:,:,1] * mask,
                            image[:,:,2] * mask))
    
    return sky_filter

def filter_image(image):
    """
    filter_image - changes the sky to white and keeps the rest the same
    
    image: np.ndarray - 3D tensor representing image
    
    Returns: filtered image : np.ndarray
    """

    sky_filter = make_sky_filter(image)
    masked_pixels = np.all(sky_filter != [0, 0, 0], axis=2) # the sky filter does not include the color black, so this works
    image_copy = image.copy()
    image_copy[masked_pixels] = (255, 255, 255) # white, change to (255, 0, 255) for testing purposes to see the background better

    return image_copy

def confirm(message):
    print(message)
    while 1:
        inp = input("y/n: ")
        if len(inp) > 0 and inp[0].lower() in {"y", "n"}:
            return inp[0].lower() == "y"

def filter_path(path):
    """
    filter_path - filters images in path, saves to OUT_DIR

    path: string - path to image or directory of images

    Returns: None
    """

    if not os.path.exists(path):
        print(f"{path} does not exist")
        exit(0)

    files = []

    # check single file
    if not os.path.isdir(path):
        files.append(path)
    else:
        for f in os.listdir(path):
            files.append(f)

    out_dir = os.path.join(os.getcwd(), OUT_DIR)

    # check if output folder exists
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    else:
        if not confirm(f"WARNING: {out_dir} already exists, risk of overwriting files. Would you still like to proceed?"):
            exit(0)

    # actual image processing
    for f in files:
        image = imread(f)
        filtered_image = filter_image(image)
        name = os.path.basename(f)
        imsave(os.path.join(out_dir, name), filtered_image)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to image or image directory")
    args = parser.parse_args()

    filter_path(args.path)

if __name__ == "__main__":
    main()
