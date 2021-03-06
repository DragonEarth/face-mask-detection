# Using Keras to load our model and images
from keras.models import load_model
from keras.preprocessing import image

# To grab environment variables, image directories, and image paths
import os
from os.path import isfile, join

# To sort our image directories by natural sort
from natsort import os_sorted

# To turn our lists into numpy arrays
import numpy as np

# Stops TF optimization warnings from displaying
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Path to dataset, to model, and to save/load history of model
DATASET_PATH = './data'
MODEL_PATH = 'face_mask_model'
HISTORY_PATH = MODEL_PATH + '/history.joblib'

# Target size our model was trained on
TARGET_SIZE = (150, 150)

# Image and Directory path to be used by our functions
IMAGE_DIRECTORY_PATH = '/full/path/here/'
# Replace IMAGE_DIRECTORY_PATH if image is not inside of image directory
IMAGE_PATH = IMAGE_DIRECTORY_PATH + 'imageNameHere.jpg'

# Loading in our previously trained model using joblib
model = load_model(MODEL_PATH)


# Returns a True/False in respect to whether the model predicts the person is wearing a mask
def predict_image(image_path):
    # Load in image and set target size to what model was trained on
    image_data = image.load_img(image_path, target_size=TARGET_SIZE)

    # Convert to a numpy array, rescales to what we trained our model on and adds additional level of nesting
    image_array = np.array(image_data)
    image_array = image_array / 255.0
    image_batch = np.expand_dims(image_array, axis=0)

    # Gets prediction of passed image
    prediction = (model.predict(image_batch) > 0.5).astype("int32")

    # True if wearing a mask - False if not
    return prediction[0] == 0.0


# Returns 2D array in respect to each image in the directory predicted to be wearing a mask as True/False & image name
def predict_directory(directory_path):
    image_list = os_sorted([f for f in os.listdir(directory_path) if isfile(join(directory_path, f))])
    predictions = []

    for image_name in image_list:
        # Load in image from directory list joined with directory path and set target size to what model was trained on
        image_data = image.load_img(directory_path + image_name, target_size=TARGET_SIZE)

        # Convert to a numpy array, rescales to what we trained our model on and adds additional level of nesting
        image_array = image.img_to_array(image_data)
        image_array = image_array / 255.0
        image_batch = np.expand_dims(image_array, axis=0)

        # Gets prediction of passed image
        prediction = (model.predict(image_batch) > 0.5).astype("int32")

        # Appends array of size 2 with True if wearing a mask - False if not & image name i.e. [True, image1.jpg]
        predictions.append([prediction[0][0] == 0.0, image_name])

    return predictions


if __name__ == '__main__':
    print(predict_image(IMAGE_PATH))
    print(predict_directory(IMAGE_DIRECTORY_PATH))
