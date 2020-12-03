import numpy as np
import cv2
import os
from keras.preprocessing import image


def classify_object(filtered_contour_objects, stacked_image, cnn_model, destination_path, slide_name):
    for coord in filtered_contour_objects:
        # We extract the rois for each focal plane by coordinates from the CZI file
        #roi_rgb2 = image_stacked[coord[0]:coord[1], coord[2]:coord[3]]

        roi_rgb = stacked_image[coord[0]-25:coord[1]-25+50, coord[2]-25:coord[3]-25+50]
        roi_rgb2 = stacked_image[coord[0]-25:coord[1]-25+50, coord[2]-25:coord[3]-25+50]
        try:
            roi_rgb2 = cv2.resize(roi_rgb2, (350, 150))

            # print (img)
            img_tensor = image.img_to_array(roi_rgb2)
            img_tensor = np.expand_dims(img_tensor, axis=0)
            # Remember that the model was trained on inputs
            # that were preprocessed in the following way:
            img_tensor /= 255.

            # # Its shape is (1, 150, 150, 3)
            preds = cnn_model.predict(img_tensor)
            #print (preds)
            #file_name = str(coord[4]) + '_' + str(coord[0]) + '_' + str(coord[1]) + '_' + str(coord[2]) + '_' + str(
                #coord[3]) + '_' + slide_name + '.png'
            file_name = str(coord[4]) + '_' +  str(round(preds[0][0] * 100, 2)) + '_' + slide_name + '.png'


            if round(preds[0][0] * 100, 2) == 0.0:
            #if round(preds[0][0] * 100, 2) <= 5.0:

                #file_results_name.write(str(slide_name) + ';' + str(region) + ';' + str(coord[4]) + ';' + str(round(preds[0][0] * 100, 2)) + '\n')
                cv2.imwrite(os.path.join(destination_path, file_name), roi_rgb)

                #print (round(preds[0][0] * 100, 2))
                #cv2.imshow('', roi_rgb2)
                #cv2.waitKey(0)
        except cv2.error:
            print(roi_rgb.shape)