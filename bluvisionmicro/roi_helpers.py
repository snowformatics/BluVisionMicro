import os
import pandas as pd
import numpy as np


def get_hyphae_area(destination_path):
    hyphae_area_lst = []
    for subdir, dirs, files in os.walk(destination_path):
        if subdir.endswith('0') or subdir.endswith('1'):
            # We need also zero colonies report in result file
            if len(files) == 0:
                file_name = subdir.split('\\')
                slide_name = file_name[5]
                region = file_name[6]
                hyphae_area_lst.append([slide_name, region, None, None])
            else:
                for file in files:
                    if os.path.join(subdir, file).endswith('.png'):
                        file_name = os.path.join(subdir, file).split('\\')
                        slide_name = file_name[-3]
                        region = file_name[-2]
                        area = file_name[-1].split('_')[1]
                        prediction =  file_name[-1].split('_')[0]
                        hyphae_area_lst.append([slide_name, region, area, prediction])
    return hyphae_area_lst


def calculate_avg_hyphae_area(data_lst):
    """Calculate the mean and std for hyphae per slide."""
    data = pd.DataFrame(data_lst, columns=['Slide_name', 'Region', 'Prediction%', 'Leaf_area'])
    data["Leaf_area"] = pd.to_numeric(data["Leaf_area"])
    hyphae_area_avg = data.groupby(['Slide_name', 'Region'], as_index=False).agg({'Leaf_area': ['mean', 'std', 'count']})
    hyphae_area_avg.columns = hyphae_area_avg.columns.droplevel()
    return hyphae_area_avg


def union(a, b):
  x = min(a[0], b[0])
  y = min(a[1], b[1])
  w = max(a[0]+a[2], b[0]+b[2]) - x
  h = max(a[1]+a[3], b[1]+b[3]) - y
  return (x, y, w, h)


def intersection(a, b):
  x = max(a[0], b[0])
  y = max(a[1], b[1])
  w = min(a[0]+a[2], b[0]+b[2]) - x
  h = min(a[1]+a[3], b[1]+b[3]) - y
  if w<0 or h<0: return () # or (0,0,0,0) ?
  return (x, y, w, h)


def combine_boxes(boxes):
    new_array = []
    for boxa, boxb in zip(boxes, boxes[1:]):
        if intersection(boxa, boxb):
            new_array.append(union(boxa, boxb))
        else:
            new_array.append(boxa)
    return np.array(new_array).astype('int')


# boxes = [[55, 67, 10, 10], [54, 66, 198, 114],
#         [49, 75, 203, 125], [42, 78, 186, 126],
#          [31, 69, 201, 125], [18, 63, 235, 135],
#          [50, 72, 197, 121], [54, 72, 198, 120],
#          [38, 65, 10, 10], [36, 60, 180, 108]]

#print (len(combine_boxes(boxes)))