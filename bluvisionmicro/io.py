import os
import cv2
import pandas
import csv

def create_folders(path_to_creat):
    if not os.path.exists(path_to_creat):
        os.makedirs(path_to_creat)


def save_image(image_name, image):
    cv2.imwrite(image_name, image)


def write_csv(data_lst, file_name, header):
    # print (data_lst)
    # pd = pandas.DataFrame(data_lst)
    # print (pd)
    # pd.to_csv(file_name)
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for data in data_lst:
            writer.writerows(data)
    # csv_file = open(file_name, 'w')
    #for data in data_lst:
    #     for subdata in data:
