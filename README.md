# BluVisionMicro

We have developed the BluVision image analysis Framework for studying plant-pathogen interactions on microscopic level. The system is build to study the life cycle of the important barley and wheat pathogen powdery mildew by collecting and analyzing image data from three key developmental stages.

BluVision is a software and hardware framework for high-throughput image acquisition and analysis of microscopic images in plant pathology. The microscopic module is based on a state of the art high-throughput microscope scanner (Zeiss Axio Scan.Z1). 

<img src="https://github.com/snowformatics/GSOC/blob/master/Bild9.png" width="70%" height="70%"><br>
Figure 1: Zeiss Axio Scan.Z1

Our image analysis pipeline is aimed to detect and analyze microscopic infection events (Figure 2 & 3).

<img src="https://github.com/snowformatics/GSOC/blob/master/Slide3.PNG" width="70%" height="70%"><br>
Figure 2:  BluVision Micro Module

<img src="https://github.com/snowformatics/GSOC/blob/master/Slide2.PNG" width="70%" height="70%"><br>
Figure 3: Blumeria graminis hyphae detetcion

## Installation

We recoommend to install the software via Ananconda:

1.) Create new enviroment with Python 3.6

conda create -n bluvision_micro python=3.6

2.) Install dependencies:

pip install numpy<br>
pip install pandas<br>
pip install czifile<br>
pip install mahotas<br>
pip install -U scikit-image<br>
pip install tensorflow<br>
pip install keras<br>
pip install opencv-contrib-python<br>
pip install scikit-learn<br>
pip to install joblib<br>

3.) Clone Github repository

git clone https://github.com/snowformatics/BluVisionMicro.git

## Run Analysis
-> Inside BluVisionMicro folder<br>
For small colonies (< 50hai):<br>
python cli.py -s source_path -d destination_path -p mildew_small -m analysis -se 0.05

For large colonies (> 50hai):<br>
python cli.py -s source_path -d destination_path -p mildew_large -m analysis -se 0.05

## Run Results

python cli.py -s source_path -d destination_path -p mildew -m results

## Parameters

-s -> path to source CZI images<br>
-d -> path to store the results<br>
-p -> pathogen, currently only mildew available <br>
-m -> mode (analysis or results)<br>
-se -> Sensitivity for the CNN to predict hyphae. We recommend using strict values for host interactions (se = 0.0) and relaxed values for nonhost interactions (0.05). <br>


