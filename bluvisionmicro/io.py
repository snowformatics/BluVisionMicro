import os
import cv2


def create_folders(path_to_creat):
    if not os.path.exists(path_to_creat):
        os.makedirs(path_to_creat)


def save_image(image_name, image):
    cv2.imwrite(image_name, image)