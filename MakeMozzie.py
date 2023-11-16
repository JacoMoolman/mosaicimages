import pathlib
import json
import os
import math
import random

import numpy as np
import cv2

# Configuration variables. Play with these.
H1 = 50
W1 = 50
KNUM = 25  #Local Randomness
MAX_USES_PER_IMAGE = 7  # Set this to your preferred limit
alpha = 0.3 # Transparency level for overleyed image.
ImageName="rb.jpg"  #This is the main image
MAINIMAGE="E:\\Projects\\MOZIECODE2\\PhotoMosaic-main\\PhotoMosaic-main\\"+ImageName
PHOTOSETS="E:\\Projects\\MOZIECODE2\\PhotoMosaic-main\\PhotoMosaic-main\\animals" #This is where all the "small" photos is 

def get_average_color(img):
    average_color = np.average(np.average(img, axis=0), axis=0)
    average_color = np.around(average_color, decimals=-1)
    average_color = tuple(int(i) for i in average_color)
    return average_color

def get_closest_colors(color, colors, k):
    cr, cg, cb = color
    color_differences = []

    for c in colors:
        r, g, b = eval(c)
        difference = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        color_differences.append((difference, c))

    color_differences.sort()  
    top_k_colors = color_differences[:k] 
    return top_k_colors

image_usage_count = {}

if "cache.json" not in os.listdir():
    imgs_dir = pathlib.Path(PHOTOSETS)
    images = list(imgs_dir.glob("**/*.jpg"))

    data = {}
    image_usage_count = {}  
    for img_path in images:
        print(".")
        img = cv2.imread(str(img_path))
        average_color = get_average_color(img)
        img_path_str = str(img_path.resolve())  
        if str(tuple(average_color)) in data:
            data[str(tuple(average_color))].append(img_path_str)
        else:
            data[str(tuple(average_color))] = [img_path_str]
        image_usage_count[img_path_str] = 0  

    with open("cache.json", "w") as file:
        json.dump(data, file, indent=2, sort_keys=True)
    print("Caching done")
else:
    with open("cache.json", "r") as file:
        data = json.load(file)
        for img_list in data.values():
            for img_path_str in img_list:
                if img_path_str not in image_usage_count:
                    image_usage_count[img_path_str] = 0


img = cv2.imread(MAINIMAGE)
img_height, img_width, _ = img.shape
tile_height, tile_width = H1, W1
num_tiles_h, num_tiles_w = img_height // tile_height, img_width // tile_width
img = img[:tile_height * num_tiles_h, :tile_width * num_tiles_w]


tiles = []
for y in range(0, img_height, tile_height):
    for x in range(0, img_width, tile_width):
        tiles.append((y, y + tile_height, x, x + tile_width))


for tile in tiles:
    y0, y1, x0, x1 = tile
    try:
        tile_slice = img[y0:y1, x0:x1]
        if tile_slice.size == 0:
            continue  

        average_color = get_average_color(tile_slice)
        top_k_colors = get_closest_colors(average_color, data.keys(), KNUM)

        eligible_colors = [(dist, color) for dist, color in top_k_colors if image_usage_count[random.choice(data[str(color)])] < MAX_USES_PER_IMAGE]
        if not eligible_colors:
            continue

        weights = [1 / (dist + 0.001) for dist, _ in eligible_colors]
        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]
        chosen_color = random.choices([color for _, color in eligible_colors], weights=probabilities, k=1)[0]

        chosen_image = random.choice([img for img in data[str(chosen_color)] if image_usage_count[img] < MAX_USES_PER_IMAGE])
        image_usage_count[chosen_image] += 1

        i = cv2.imread(chosen_image)
        i = cv2.resize(i, (tile_width, tile_height))
        img[y0:y1, x0:x1] = i

    except Exception as e:
        print(f"Error processing tile at {y0},{x0}: {e}")
        continue


cv2.namedWindow("Image", cv2.WINDOW_NORMAL)


max_size = 1000
aspect_ratio = img_width / img_height
if img_width > img_height:
    display_width = min(img_width, max_size)
    display_height = int(display_width / aspect_ratio)
else:
    display_height = min(img_height, max_size)
    display_width = int(display_height * aspect_ratio)
cv2.resizeWindow("Image", display_width, display_height)

cv2.imshow("Image", img)
cv2.waitKey(1)

original_img = cv2.imread(MAINIMAGE)

img_resized_for_overlay = cv2.resize(img, (original_img.shape[1], original_img.shape[0]))

overlay_img = cv2.addWeighted(img_resized_for_overlay, 1 - alpha, original_img, alpha, 0)

cv2.imshow("Image", overlay_img)
cv2.waitKey(1)
outputfile=ImageName+"overley.jpg"
cv2.imwrite(outputfile, overlay_img)