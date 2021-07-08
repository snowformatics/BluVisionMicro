import os
import cv2
import pandas as pd


def create_folders(path_to_create):
    if not os.path.exists(path_to_create):
        os.makedirs(path_to_create)


def save_image(image_name, image):
    cv2.imwrite(image_name, image)


def draw_rectangle_on_image(image, lst_of_rois):
    imgage_rectangles = image.copy()
    for roi in lst_of_rois:
        cv2.rectangle(imgage_rectangles, (roi[0], roi[1]), (roi[2], roi[3]), (0, 0, 255), 2)
    return imgage_rectangles


def write_csv(data, file_name, header):

    if isinstance(data, list):
        df = pd.DataFrame(data, columns=header)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        df = data
        df.columns = header
    df.to_csv(file_name, index=False, sep=';')


