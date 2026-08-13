from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np


# Function to preprocess the image for prediction
def preprocess_image(image_path):
    # Load the trained model
    loaded_model = load_model("smith1.h5")  # Use the path where you saved your trained model

    img = image.load_img(image_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the image



    # Make predictions
    predictions = loaded_model.predict(img_array)

    # Map predicted class index to label
    class_labels = ['BACTERIAL','Bengin cases','COVID','Malignant cases', 'NORMAL','Normal cases','TUBER','VIRAL']
    predicted_class_index = np.argmax(predictions)
    predicted_class_label = class_labels[predicted_class_index]

    print("Predicted Class:", predicted_class_label)
    return predicted_class_label







# # coding: utf-8

# # In[ ]:
# import os


# import tensorflow as tf

# import keras
# from keras.engine.saving import load_model
# from keras.models import Sequential
# from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
# from keras.layers import Dense, Activation, Dropout, Flatten

# from keras.preprocessing import image
# from keras.preprocessing.image import ImageDataGenerator

# import numpy as np
# from keras import backend as K
# # from camara import *
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



# def read_dataset1(path):
#     data_list = []
#     label_list = []

#     file_path = os.path.join(path)
#     print(file_path)
#     img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#     res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
#     data_list.append(res)
#     # label = dirPath.split('/')[-1]

#             # label_list.remove("./training")
#     return (np.asarray(data_list, dtype=np.float32))

# def predictcnn(ff):
#     # captures()
#     # fn="static/newimg.jpg"
#     K.clear_session()

#     # fn="train/Cyst/Cyst- (1).jpg"
#     dataset=read_dataset1(ff)
#     (mnist_row, mnist_col, mnist_color) = 48, 48, 1

#     dataset = dataset.reshape(dataset.shape[0], mnist_row, mnist_col, mnist_color)
#     mo = load_model("model1.h5")
#     dataset /= 255

#     # predict probabilities for test set

#     yhat_classes = mo.predict_classes(dataset, verbose=0)
#     # print(yhat_classes)
#     K.clear_session()

#     return yhat_classes[0]

# #
# #     print(yhat_classes)

# fn="Tr-gl_0010.jpg"
# s=predictcnn(fn)
# print(s)

# Function to evaluate model performance on a dataset

# from sklearn.metrics import classification_report, confusion_matrix
# import os
# def evaluate_model(dataset_path):
#     # Define lists to store true and predicted labels
#     true_labels = []
#     predicted_labels = []

#     # Loop through images in the dataset
#     for image_filename in os.listdir(dataset_path):
#         image_path = os.path.join(dataset_path, image_filename)
#         true_label = image_filename.split("_")[0]
#         true_labels.append(true_label)

#         # Preprocess the image and make predictions
#         predicted_label = preprocess_image(image_path)
#         predicted_labels.append(predicted_label)

#     # Calculate precision, recall, F1-score, and confusion matrix
#     print("\nClassification Report:")
#     print(classification_report(true_labels, predicted_labels))

#     print("\nConfusion Matrix:")
#     print(confusion_matrix(true_labels, predicted_labels))

# dataset_path = dataset_path = r"D:\Adarsh_Jin\mds_final\medical_delivery_system\medical_delivery_system\train"
# evaluate_model(dataset_path)


# import os
# import cv2
# import numpy as np
# from keras.engine.saving import load_model
# from keras.models import Sequential
# from keras.layers import Conv2D, Dense, Flatten
# from keras import backend as K

# def read_dataset1(path):
#     data_list = []

#     file_path = os.path.join(path)
#     img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
#     res = cv2.resize(img, (48, 48), interpolation=cv2.INTER_CUBIC)
#     data_list.append(res)
#     return np.asarray(data_list, dtype=np.float32)

# def predict_cnn(ff):
#     K.clear_session()

#     dataset = read_dataset1(ff)
#     (mnist_row, mnist_col, mnist_color) = 48, 48, 1
#     dataset = dataset.reshape(dataset.shape[0], mnist_row, mnist_col, mnist_color)
#     dataset /= 255

#     # Define your model architecture here
#     model = Sequential()
#     model.add(Conv2D(32, (3, 3), input_shape=(48, 48, 1), activation='relu'))
#     model.add(Conv2D(64, (3, 3), activation='relu'))
#     model.add(Flatten())
#     model.add(Dense(128, activation='relu'))
#     model.add(Dense(64, activation='relu'))
#     # Add other layers as per the saved model architecture
#     # ...

#     # Load the saved model
#     mo = load_model("model1.h5")

#     # Ensure that the model has the same number of classes as the original training
#     num_classes = 4  # Update with the correct number of classes

#     # If the original model was trained with categorical crossentropy, use softmax activation in the last layer
#     model.add(Dense(num_classes, activation='softmax'))

#     # Compile the model
#     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#     # Load the weights into the model
#     model.set_weights(mo.get_weights())

#     # Predict probabilities for the test set
#     yhat_classes = model.predict_classes(dataset, verbose=0)

#     return yhat_classes[0]

# # Example usage
# fn = "Tr-gl_0010.jpg"
# prediction = predict_cnn(fn)
# print(prediction)
