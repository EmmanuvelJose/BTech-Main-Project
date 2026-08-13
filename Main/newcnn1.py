import os
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Set random seed for reproducibility
seed = 42
np.random.seed(seed)
# tf.random.set_seed(seed)
# tf.random.set_random_seed(1)
tf.random.set_seed(1)
# random.seed(seed)
import tensorflow
# tensorflow.random.set_seed(seed)
# tf.random.set_random_seed(1)

# Set the paths to your dataset
train_dir = r"D:\Adarsh_Jin\mds_final\medical_delivery_system\medical_delivery_system\train"
validation_dir = r"D:\Adarsh_Jin\mds_final\medical_delivery_system\medical_delivery_system\train"

# model_save_path = "model_new.h5"  # Specify the path to save the trained model
model_save_path = "abdvi.h5"

# Define image dimensions and batch size
img_width, img_height = 150, 150
batch_size = 32

# Create data generators with data augmentation for the training set
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Rescale validation set
validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Create generators for reading images from the directories
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical'
)

# Define the CNN model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(img_width, img_height, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(8, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=2,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size
)

# Save the trained model
# Save the trained model
model.save(model_save_path)
print("Model saved successfully at:", model_save_path)


# Evaluate the model
accuracy = model.evaluate(validation_generator)[1]
print(f"Validation Accuracy: {accuracy * 100:.2f}%")



# Validation Accuracy: 98.56%

# Get the summary of the trained model
model.summary()



# # coding: utf-8

# # In[ ]:
# import os

# import tensorflow as tf
# # sess = tf.Session()
# import keras
# from keras.engine.saving import load_model
# from keras.models import Sequential
# from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
# from keras.layers import Dense, Activation, Dropout, Flatten

# from keras.preprocessing import image
# from keras.preprocessing.image import ImageDataGenerator

# import numpy as np

# #------------------------------
# # sess = tf.Session()
# # keras.backend.set_session(sess)
# #------------------------------
# #variables
# num_classes =4
# batch_size = 40
# epochs = 5
# #------------------------------

# import os, cv2, keras
# import numpy as np
# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Flatten
# from keras.layers import Conv2D, MaxPooling2D
# from keras.engine.saving import load_model
# # manipulate with numpy,load with panda
# import numpy as np
# # import pandas as pd

# # data visualization
# import cv2
# import matplotlib
# import matplotlib.pyplot as plt
# # import seaborn as sns

# # get_ipython().run_line_magic('matplotlib', 'inline')


# # Data Import
# def read_dataset():
#     data_list = []
#     label_list = []
#     i=0
#     my_list = os.listdir(r'Training\\')
#     for pa in my_list:

#         print(pa,"==================",i)
#         for root, dirs, files in os.walk(r'Training\\' + pa):

#          for f in files:
#             file_path = os.path.join(r'Training\\'+pa, f)
#             # print(file_path)
#             img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#             res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
#             data_list.append(res)
#             # label = dirPath.split('/')[-1]
#             label = i
#             label_list.append(label)
#         i=i+1

#     return (np.asarray(data_list, dtype=np.float32), np.asarray(label_list))

# def read_dataset1(path):
#     data_list = []
#     label_list = []

#     file_path = os.path.join(path)
#     img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#     res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
#     data_list.append(res)
#     # label = dirPath.split('/')[-1]

#             # label_list.remove("./training")
#     return (np.asarray(data_list, dtype=np.float32))

# from sklearn.model_selection import train_test_split
# # load dataset
# x_dataset, y_dataset = read_dataset()
# X_train, X_test, y_train, y_test = train_test_split(x_dataset, y_dataset, test_size=0.5, random_state=0)

# y_train1=[]
# for i in y_train:
#     emotion = keras.utils.to_categorical(i, num_classes)
#     print(i,emotion)
#     y_train1.append(emotion)

# y_train=y_train1
# x_train = np.array(X_train, 'float32')
# y_train = np.array(y_train, 'float32')
# x_test = np.array(X_test, 'float32')
# y_test = np.array(y_test, 'float32')

# x_train /= 255  # normalize inputs between [0, 1]
# x_test /= 255
# print("x_train.shape",x_train.shape)
# x_train = x_train.reshape(x_train.shape[0], 48, 48, 1)
# x_train = x_train.astype('float32')
# x_test = x_test.reshape(x_test.shape[0], 48, 48, 1)
# x_test = x_test.astype('float32')

# print(x_train.shape[0], 'train samples')
# print(x_test.shape[0], 'test samples')
# # ------------------------------
# # construct CNN structure

# model = Sequential()

# # 1st convolution layer
# model.add(Conv2D(64, (5, 5), activation='relu', input_shape=(48, 48, 1)))
# model.add(MaxPooling2D(pool_size=(5, 5), strides=(2, 2)))

# # 2nd convolution layer
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(Conv2D(64, (3, 3), activation='relu'))
# model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

# # 3rd convolution layer
# model.add(Conv2D(128, (3, 3), activation='relu'))
# model.add(Conv2D(128, (3, 3), activation='relu'))
# model.add(AveragePooling2D(pool_size=(3, 3), strides=(2, 2)))

# model.add(Flatten())

# # fully connected neural networks
# model.add(Dense(1024, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(1024, activation='relu'))
# model.add(Dropout(0.2))

# model.add(Dense(num_classes, activation='softmax'))
# # ------------------------------
# # batch process

# print(x_train.shape)

# gen = ImageDataGenerator()
# train_generator = gen.flow(x_train, y_train, batch_size=batch_size)

# # ------------------------------

# model.compile(loss='categorical_crossentropy'
#               , optimizer=keras.optimizers.Adam()
#               , metrics=['accuracy']
#               )

# # ------------------------------

# if not os.path.exists("model1.h5"):

#     model.fit_generator(train_generator, steps_per_epoch=batch_size, epochs=epochs)
#     model.save("model1.h5")  # train for randomly selected one
# else:
#     model = load_model("model1.h5")  # load weights
# from sklearn.metrics import confusion_matrix
# yp=model.predict_classes(x_test,verbose=0)
# cf=confusion_matrix(y_test,yp)
# print(cf)
# def predictcnn(fn):
#     dataset=read_dataset1(fn)
#     (mnist_row, mnist_col, mnist_color) = 48, 48, 1

#     dataset = dataset.reshape(dataset.shape[0], mnist_row, mnist_col, mnist_color)
#     mo = load_model("model1.h5")

#     # predict probabilities for test set

#     yhat_classes = mo.predict_classes(dataset, verbose=0)
#     return yhat_classes
# #
# #     print(yhat_classes)

# predict("Tr-gl_0010.jpg")
# Import necessary libraries

# abd.h5
# Validation Accuracy: 92.59%
# Model: "sequential"
# _________________________________________________________________
#  Layer (type)                Output Shape              Param #
# =================================================================
#  conv2d (Conv2D)             (None, 148, 148, 32)      896

#  max_pooling2d (MaxPooling2  (None, 74, 74, 32)        0
#  D)

#  conv2d_1 (Conv2D)           (None, 72, 72, 64)        18496

#  max_pooling2d_1 (MaxPoolin  (None, 36, 36, 64)        0
#  g2D)

#  conv2d_2 (Conv2D)           (None, 34, 34, 128)       73856

#  max_pooling2d_2 (MaxPoolin  (None, 17, 17, 128)       0
#  g2D)

#  flatten (Flatten)           (None, 36992)             0

#  dense (Dense)               (None, 128)               4735104

#  dense_1 (Dense)             (None, 8)                 1032

# =================================================================
# Total params: 4829384 (18.42 MB)
# Trainable params: 4829384 (18.42 MB)
# Non-trainable params: 0 (0.00 Byte)
# _________________________________________________________________
