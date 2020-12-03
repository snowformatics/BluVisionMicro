import numpy as np
import cv2
import os
from keras.preprocessing import image


def classify_object(filtered_contour_objects, stacked_image, cnn_model, destination_path, slide_name):
    for coord in filtered_contour_objects:
        # We extract the rois for each focal plane by coordinates from the CZI file
        roi_original = stacked_image[coord[0]-25:coord[1]-25+50, coord[2]-25:coord[3]-25+50]
        roi_resized = stacked_image[coord[0]-25:coord[1]-25+50, coord[2]-25:coord[3]-25+50]
        try:
            roi_resized = cv2.resize(roi_resized, (350, 150))
            img_tensor = image.img_to_array(roi_resized)
            img_tensor = np.expand_dims(img_tensor, axis=0)
            # Remember that the model was trained on inputs
            # that were preprocessed in the following way:
            img_tensor /= 255.
            preds = cnn_model.predict(img_tensor)
            file_name = str(coord[4]) + '_' +  str(round(preds[0][0] * 100, 2)) + '_' + slide_name + '.png'

            if round(preds[0][0] * 100, 2) == 0.0:
            #if round(preds[0][0] * 100, 2) <= 5.0:
                cv2.imwrite(os.path.join(destination_path, file_name), roi_original)
        except cv2.error:
            print(roi_original.shape)