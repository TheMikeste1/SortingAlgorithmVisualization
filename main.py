import os
from random import seed
from random import shuffle
import threading

import cv2
import numpy as np
import imageio as ioi
from pygifsicle import optimize

from sorting_steps import *

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (0, 0, 255)


def log(*message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]", end=" ")
    for arg in message:
        print(arg, end=" ")
    print()


def get_images(directory, img_types=None):
    if img_types is None:
        img_types = ["png", "jpg", "jpeg"]

    # We just want the first layer. This could use all images,
    # including those in subdirectories, by simply putting it in a loop
    _, _, files = os.walk(directory).__next__()

    for file in files:
        if file.split(".")[-1] not in img_types:
            files.remove(file)

    files.sort()
    files.sort(key=len)

    for file in files:
        img = ioi.imread(directory + "/" + file)
        yield img


def gen_blank_image(height, width):
    return np.zeros((height, width, 3), dtype=np.uint8)


def gen_elements_image(iterable, height=-1, width=-1, scale=1):
    if height < 0:
        height = max(iterable)
    if width < 0:
        width = len(iterable)
    if scale < 1:
        scale = 1

    img = gen_blank_image(height * scale, width * scale)

    # Add elements
    for i, elem in enumerate(iterable):
        # -Y, X
        img[(height - elem) * scale:, i * scale:i * scale + scale] = WHITE

    return img


def gen_highlighted_image(iterable, s1, s2, color, height=-1, width=-1, scale=1):
    if height < 0:
        height = max(iterable)
    if width < 0:
        width = len(iterable)
    if scale < 1:
        scale = 1

    img = gen_elements_image(iterable, height, width, scale=scale)

    # Highlight selected
    length = (height - iterable[s1]) * scale
    start = s1 * scale
    img[length:, start:start + scale] = color

    length = (height - iterable[s2]) * scale
    start = s2 * scale
    img[length:, start:start + scale] = color

    return img


def output_img(iterable, s1, s2, color, output_filename, height=-1, width=-1, scale=1):
    img = gen_highlighted_image(iterable, s1, s2, color, height=height, width=width, scale=scale)
    cv2.imwrite(output_filename, img)


def main():
    # Settings
    num_generated = 15
    height = -1
    width = -1

    seed(314159)

    sort_function = heapsort_stepped

    output = sort_function.__name__
    filetype = "png"
    scale = 20

    log("Setting up...")
    # Generate the numbers
    sorted_list = list(range(1, num_generated + 1))

    # Shuffle
    shuffle(sorted_list)

    # Setup
    image_num = 0
    generator = sort_function(sorted_list.copy())
    filetype = filetype.lower()

    # Output Setup
    output_dir = os.path.join(os.getcwd(), output)
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        for dir_, subdir, files in os.walk(output_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(dir_, file))
            os.rmdir(dir_)
        os.mkdir(output_dir)

    os.mkdir(output_dir + "/images")

    log("Outputting images to", output_dir + "\\images", "as", filetype)

    filetype = "." + filetype

    # Create initial image
    current_list = sorted_list

    img = gen_elements_image(sorted_list, height=height, scale=scale)
    cv2.imwrite(output_dir + "/images/" + str(image_num) + filetype, img)
    image_num += 1

    # Begin sort
    threads = []
    log("Beginning sort")
    while True:
        # Get next step
        try:
            current_list, s1, s2, swapped = generator.__next__()
        except StopIteration as out:
            log("Elements:", len(out.value[0]))
            log("Compares:", out.value[1])
            log("Swaps:", out.value[2])
            log("Sorting time taken:", out.value[3])
            break

        # Create selection image
        output_filename = output_dir + "/images/" + str(image_num) + filetype
        image_num += 1
        threads.append(threading.Thread(target=output_img,
                                        args=(sorted_list.copy(), s1, s2, GREEN, output_filename, height, width, scale)
                                        )
                       )
        threads[-1].start()

        # If we swapped, make swap image
        if swapped:
            sorted_list = current_list.copy()
            output_filename = output_dir + "/images/" + str(image_num) + filetype
            image_num += 1
            threads.append(threading.Thread(target=output_img,
                                            args=(
                                                sorted_list.copy(), s1, s2, RED, output_filename, height, width, scale)
                                            )
                           )
            threads[-1].start()
    log("End sort")

    # Generate final image
    img = gen_elements_image(current_list, height=height, scale=scale)
    cv2.imwrite(output_dir + "/images/" + str(image_num) + filetype, img)

    log("Waiting on threads...")
    for thread in threads:
        thread.join()

    log("Creating GIF at", output_dir)

    generator = get_images(output_dir + "/images/")
    filename = output_dir + "\\" + output + ".gif"
    ioi.mimwrite(filename, generator)

    log("File size:", os.path.getsize(filename))

    log("Optimizing GIF...")
    optimize(filename)
    log("Optimized file size:", os.path.getsize(filename))
    log("Finished")
    return


if __name__ == '__main__':
    main()
