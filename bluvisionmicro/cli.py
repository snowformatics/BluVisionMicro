import argparse
import os
import numpy as np
from keras.models import load_model
from joblib import Parallel, delayed
from bluvisionmicro.hyphae_pipeline import HyphaePipeline
from bluvisionmicro.results_pipeline import ResultsPipeline

import bluvisionmicro.io

parser = argparse.ArgumentParser(description='BluVision Micro analysis software.')
parser.add_argument('-s', '--source_path', required=True,
                    help='Directory containing images to segment.')
parser.add_argument('-d', '--destination_path', required=True,
                    help='Directory to store the result images.')
parser.add_argument('-p', '--pathogen', required=True,
                    help='Pathogen')
parser.add_argument('-m', '--mode', required=True,
                    help='Software mode.')
parser.add_argument('-se', '--sensitivity', required=False,
                    help='sensitivity to predict hyphae objects.')




# We get all the arguments from the user input
args = parser.parse_args()
# Folder structure example
# D:\Mikroskop\slides\HA0077\48hai
# Source Path =            D:\Mikroskop\slides\
# Experiment name =        HA0077
# inoculation time point = 48hai

# Source path with experiments
source_path = args.source_path

# Path to store the results
destination_path = args.destination_path
# Load pathogen mode
pathogen = args.pathogen
# Load software mode
mode = args.mode
# Sensitivity to predict hyphae objects.
sensitivity = args.sensitivity
# List of experiments
experiments = os.listdir(source_path)
print (source_path, experiments)
# Load CNN Model for prediction
cnn_model = load_model('09112020_1.h5')
#cnn_model = load_model('C:/Users/lueck/PycharmProjects/cnn_tuner/best.h5')

#cnn_model = None

# Connect segmenter class to the pathogen argument
segmenter_class = {
    'mildew': HyphaePipeline
}.get(pathogen)
if not segmenter_class:
    raise argparse.ArgumentError("Invalid segmentation method '{}'".format(pathogen))
print (segmenter_class)
# Image analysis mode

for experiment in experiments:
    # Experiments can have several pathogen inoculation time points
    # We loop over each inoculation time point inside the experiment
    hais = os.listdir(os.path.join(source_path, experiment))
    print (experiment, hais)
    for hai in hais:

        if hai.find('hai') != -1 and not hai.endswith('.txt'):

            # We create a Label folder inside the destination experiment folder where we store the CZIfile labels
            #bluvisionmicro.io.create_folders(os.path.join(destination_path, experiment, hai, 'Label'))
            # We get all CZI images inside for the particular inoculation time point
            images = os.listdir(os.path.join(source_path, experiment, hai))
            print (images)
            data = [(slide_name, cnn_model, source_path, destination_path, experiment, hai, sensitivity) for slide_name in images if slide_name.endswith('.czi')]
            if len(data) > 10:
                image_sub_lst = np.array_split(data, len(data) / 6)
            else:
                image_sub_lst = np.array_split(data, 1)
            print (len(image_sub_lst))
            if mode == "analysis":
                print(mode)
                # Single
                # for sub_lst in image_sub_lst:
                #     for i in sub_lst:
                #         print (i)
                #         segmenter_class().start_pipeline(i)
                # Mulit
                for sub_lst in image_sub_lst:
                    print (sub_lst)
                    Parallel(n_jobs=8)(delayed(segmenter_class().start_pipeline)(i) for i in sub_lst)

            # Result mode after cleaning false positives
            elif mode == "results":
                print (mode)
                args = [images, source_path, destination_path, experiment, hai]
                bluvisionmicro.results_pipeline.ResultsPipeline().start_pipeline(args)







