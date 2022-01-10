import numpy as np
import pickle
import cv2
from os import listdir
from sklearn.preprocessing import LabelBinarizer
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation, Flatten, Dropout, Dense
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import resource

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))

def convert_image_to_array(image_dir, default_image_size):
    try:
        image = cv2.imread(image_dir)
        if image is not None:
            image = cv2.resize(image,default_image_size)
            return img_to_array(image)
        else:
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None

def main():
    limit_memory(10000000000)
    EPOCHS = 2
    INIT_LR = 1e-3
    BS = 32
    default_image_size = tuple((256, 256))
    image_size = 0
    directory_root = '/tf/mydata/data/PlantVillage/PlantVillage/'
    width=256
    height=256
    depth=3
    image_list, label_list = [], []
    try:
        print("[INFO] Loading images ...")
        root_dir = listdir(directory_root)
        print(root_dir)

        #Looping inside root_directory
        for directory in root_dir :
            # remove .DS_Store from list
            if directory == ".DS_Store" :
                root_dir.remove(directory)

        for plant_folder in root_dir :
            plant_disease_folder_list = listdir(f"{directory_root}/{plant_folder}")
            print(f"[INFO] Processing {plant_folder} ...")

            #looping in images
            for disease_folder in plant_disease_folder_list :
                # remove .DS_Store from list
                if disease_folder == ".DS_Store" :
                    plant_disease_folder_list.remove(plant_folder)

            #If all data taken not able to train
            for images in plant_disease_folder_list:
                image_directory = f"{directory_root}/{plant_folder}/{images}"
                if image_directory.endswith(".jpg") == True or image_directory.endswith(".JPG") == True:
                    image_list.append(convert_image_to_array(image_directory, default_image_size))
                    label_list.append(plant_folder)

        print("[INFO] Image loading completed")  
    except Exception as e:
        print(f"Error : {e}")

    image_size = len(image_list)
    label_binarizer = LabelBinarizer()
    image_labels = label_binarizer.fit_transform(label_list)

    pickle.dump(label_binarizer,open('label_transform.pkl','wb'))
    n_classes = len(label_binarizer.classes_)
    print(label_binarizer.classes_)

    np_image_list = np.array(image_list, dtype = np.float)/255.0
    print('Splitting data to train,test')
    x_train = np_image_list
    y_train = image_labels

    aug = ImageDataGenerator(
        rotation_range = 25, width_shift_range=0.1,
        height_shift_range=0.1, shear_range=0.2,
        zoom_range=0.2, horizontal_flip = True,
        fill_mode="nearest")

    model = Sequential()
    inputShape = (height, width, depth)
    chanDim = -1
    if K.image_data_format() == "channels_first":
        inputShape = (depth, height, width)
        chanDim = 1

    model.add(Conv2D(32, (3, 3), padding="same",input_shape=inputShape))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(3, 3)))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(64, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Conv2D(128, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(Conv2D(128, (3, 3), padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(axis=chanDim))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())

    model.add(Dense(32))
    model.add(Activation("relu"))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(n_classes))
    model.add(Activation("softmax"))

    model.compile(loss="binary_crossentropy", optimizer = "Adam", metrics=["accuracy"])
    print("Training Model.....")
    history = model.fit_generator(
            aug.flow(x_train, y_train, batch_size= BS),
            # validation_data = (x_test, y_test),
            steps_per_epoch = len(x_train) // BS,
            epochs = EPOCHS, verbose = 1
            )
            
if __name__ == '__main__':
    main()