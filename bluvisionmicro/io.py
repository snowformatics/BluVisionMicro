import os
import cv2
import pandas as pd
import csv


def create_folders(path_to_create):
    if not os.path.exists(path_to_create):
        os.makedirs(path_to_create)


def save_image(image_name, image):
    cv2.imwrite(image_name, image)


def write_csv(data_lst, file_name, header):
    if isinstance(data_lst, list):
        df = pd.DataFrame(data_lst, columns=header)
    else:
        df = data_lst
        df.columns = header
    df.to_csv(file_name, index=False, sep=';')


