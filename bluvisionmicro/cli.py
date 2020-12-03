import argparse
import os
from keras.models import load_model
from bluvisionmicro.hyphae_pipeline import HyphaePipeline


parser = argparse.ArgumentParser(description='BluVision Micro analysis software.')
parser.add_argument('-s', '--source_path', required=True,
                    help='Directory containing images to segment.')
parser.add_argument('-d', '--destination_path', required=True,
                    help='Directory to store the result images.')
parser.add_argument('-p', '--procedure', required=True,
                    help='Pathogen')


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
# List of experiments
experiments = os.listdir(source_path)
# Load CNN Model for prediction
#cnn_model = load_model('09112020_1.h5')
cnn_model = None



procedure = args.procedure
segmenter_class = {
    'mildew': HyphaePipeline
}.get(procedure)
if not segmenter_class:
    raise argparse.ArgumentError("Invalid segmentation method '{}'".format(procedure))

for experiment in experiments:
    # Experiments can have several pathogen inoculation time points
    # We loop over each inoculation time point inside the experiment
    hais = os.listdir(os.path.join(source_path, experiment))
    for hai in hais:

        # We get all CZI images inside for the particular inoculation time point
        images = os.listdir(os.path.join(source_path, experiment, hai))
        print (images)
        for slide_name in images:
            #read_czi_image(os.path.join(source_path, experiment, hai), slide_name)
            args = [slide_name, cnn_model, source_path, destination_path, experiment, hai]
            segmenter_class().start_pipeline(args)
