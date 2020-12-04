import os
import pandas as pd


def get_hyphae_area(destination_path):
    hyphae_area_lst = []
    for subdir, dirs, files in os.walk(destination_path):
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
