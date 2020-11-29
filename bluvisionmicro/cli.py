import argparse

parser = argparse.ArgumentParser(description='BluVision Micro analysis software.')
parser.add_argument('-s', '--source_path', required=True,
                    help='Directory containing images to segment.')
parser.add_argument('-d', '--destination_path', required=True,
                    help='Directory to store the result images.')


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


for experiment in experiments:
    # Experiments can have several pathogen inoculation time points
    # We loop over each inoculation time point inside the experiment
    dais = os.listdir(os.path.join(source_path, experiment))
    for hai in dais:


        # We get all CZI images inside for the particular inoculation time point
        images = os.listdir(os.path.join(source_path, experiment, hai))
