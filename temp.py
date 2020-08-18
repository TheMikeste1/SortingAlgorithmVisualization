"""
Course: CS312
File: teach1.py
Description:
   OpenCV functions

   You are NOT submitting this program.
"""

"""
Instructions:

- You will impliementing the following functions using Opencv
- The first step is to make sure that you have OpenCV for Python installed
- You a free to use any images for the function below (except task 5)
  - Download images from the Internet
  - Use your own photos
- You must download "usa.png" from the GitHub repo for task 5

"""
import numpy as np
import cv2
from matplotlib import pyplot as plt


def task1():
    """ task1: load and display an image """
    image = cv2.imread("usa.png")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()


def task2():
    """ Task2: Open image and flip left <-> right """

    # 1) Try doing this task using loops and just the numpy array once you load the image
    image = cv2.imread("usa.png")

    flipped_image = image.copy()[:, ::-1]

    plt.imshow(cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB))
    plt.title("Flipped using NumPy")
    plt.show()

    # 2) Use OpenCV function(s)
    opencv_flipped_image = cv2.flip(image.copy(), 1)

    plt.imshow(cv2.cvtColor(opencv_flipped_image, cv2.COLOR_BGR2RGB))
    plt.title("Flipped using OpenCV")
    plt.show()


def task3():
    """ Task3: Open image and flip up <-> down """

    # 1) Try doing this task using loops and just the numpy array once you load the image
    image = cv2.imread("usa.png")

    flipped_image = image.copy()[::-1]
    plt.imshow(cv2.cvtColor(flipped_image, cv2.COLOR_BGR2RGB))
    plt.title("Flipped using NumPy")
    plt.show()

    # 2) Use OpenCV function(s)
    opencv_flipped_image = cv2.flip(image.copy(), 0)

    plt.imshow(cv2.cvtColor(opencv_flipped_image, cv2.COLOR_BGR2RGB))
    plt.title("Flipped using OpenCV")
    plt.show()

    print('Task 3')


def task4():
    """ Task4: Resample image down 50% """

    # Do this task using loops and just the numpy array once you load the image
    image = cv2.imread("usa.png")

    downsized_image = image.copy()[::2, ::2]

    plt.imshow(cv2.cvtColor(downsized_image, cv2.COLOR_BGR2RGB))
    plt.title("Resampled 50%")
    plt.show()


def task5():
    """ Task5: Tile a small image into a larger one """

    # load 'usa.png' and create a large 400 x 600 tiled image
    horizontal = 400
    vertical = 600
    usa = cv2.imread("usa.png")
    tiled = np.empty((vertical, horizontal, 3), dtype=np.uint8)

    shape = np.shape(usa)

    i = 0
    while i < vertical:
        j = 0
        while j < horizontal:
            tiled[i:i + shape[0], j:j + shape[1]] = usa[:vertical - i, :horizontal - j]
            j += shape[1]
        i += shape[0]

    plt.imshow(cv2.cvtColor(tiled, cv2.COLOR_BGR2RGB))
    plt.title("Tiled")
    plt.show()


def task6():
    """ Task6: EXTRA - Tile a small image into a larger one like a brick wall """

    # load 'usa.png' and create a large 400 x 600 tiled image

    print('Task 6')


def main():
    """ Main function """

    task1()
    task2()
    task3()
    task4()
    task5()
    task6()


if __name__ == "__main__":
    # execute only if run as a script
    main()
