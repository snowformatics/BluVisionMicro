import numpy as np
import cv2
import os
from keras.preprocessing import image


def classify_object(filtered_contour_objects, stacked_image, cnn_model, destination_path, slide_name, sensitivity):
    print (destination_path)
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
            file_name = str(coord[4]) + '_' + str(round(preds[0][0] * 100, 2)) + '_' + slide_name + '.png'
            #if round(preds[0][0] * 100, 2) == 0.0:
                #cv2.imwrite(os.path.join(destination_path, file_name), roi_original)
            if float(sensitivity) == 0.00:
                if round(preds[0][0] * 100, 2) == 0.0:
                    cv2.imwrite(os.path.join(destination_path, file_name), roi_original)
            else:
                if round(preds[0][0] * 100, 2) <= float(sensitivity):
                    cv2.imwrite(os.path.join(destination_path, file_name), roi_original)
        except cv2.error:
            print(roi_original.shape)


def train_cnn():
    import cv2
    import os
    import numpy as np
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import Dropout
    from keras.layers import Flatten
    from keras.constraints import maxnorm
    from keras.optimizers import SGD
    from keras.layers.convolutional import Convolution2D
    from keras.layers.convolutional import MaxPooling2D
    from keras.utils import np_utils
    from sklearn.model_selection import train_test_split
    from imutils import paths
    import random
    import matplotlib.pyplot as plt

    data = []
    labels = []

    # grab the image paths and randomly shuffle them
    imagePaths = sorted(list(paths.list_images("C:/06112020_hyphae/all/")))
    random.seed(42)
    random.shuffle(imagePaths)
    # loop over the input images
    for imagePath in imagePaths:
        # load the image, resize it to 350x150 pixels, and store the image in the
        # data list
        image = cv2.imread(imagePath)
        image = cv2.resize(image, (350, 150))
        data.append(image)
        # extract the class label from the image path and update the
        # labels list
        label = imagePath.split(os.path.sep)[-2].split('/')[-1]
        if label == 'pos':
            label = 1
        elif label == 'neg':
            label = 0
        labels.append(label)

    # scale the raw pixel intensities to the range [0, 1]
    data = np.array(data, dtype="float") / 255.0
    labels = np.array(labels)

    # partition the data into training and testing splits using 75% of
    # the data for training and the remaining 25% for testing
    (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.25, random_state=42)
    unique, counts = np.unique(trainY, return_counts=True)
    print(dict(zip(unique, counts)))

    y_train = np_utils.to_categorical(trainY)
    y_test = np_utils.to_categorical(testY)
    num_classes = 2

    # # # Create the model
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, input_shape=(150, 350, 3), activation='relu', border_mode='same'))
    model.add(Dropout(0.2))
    model.add(Convolution2D(32, 3, 3, activation='relu', border_mode='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Convolution2D(64, 3, 3, activation='relu', border_mode='same'))
    model.add(Dropout(0.2))
    model.add(Convolution2D(64, 3, 3, activation='relu', border_mode='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(1024, activation='relu', W_constraint=maxnorm(3)))
    model.add(Dropout(0.2))
    model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
    model.add(Dropout(0.2))
    model.add(Dense(num_classes, activation='softmax'))
    # Compile model
    epochs = 25
    lrate = 0.01
    decay = lrate / epochs
    sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    print(model.summary())

    # Fit the model
    H = model.fit(trainX, y_train, validation_data=(testX, y_test), nb_epoch=epochs, batch_size=32)
    # Final evaluation of the model
    scores = model.evaluate(testX, y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1] * 100))

    N = np.arange(0, epochs)
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(N, H.history["loss"], label="train_loss")
    plt.plot(N, H.history["val_loss"], label="val_loss")
    plt.plot(N, H.history["accuracy"], label="train_acc")
    plt.plot(N, H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy (SmallVGGNet)")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.savefig('10112020.png')
    model.save('10112020_1.h5')
