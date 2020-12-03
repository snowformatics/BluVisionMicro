import os


def create_folders(path_to_creat):
    if not os.path.exists(path_to_creat):
        os.makedirs(path_to_creat)
