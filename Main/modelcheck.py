import os
import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Load the model
model = tf.keras.models.load_model('abd.h5')

# Function to load image data and corresponding labels
def load_data(dataset_path):
    images = []
    labels = []
    class_labels = ['BACTERIAL','Bengin cases','COVID','Malignant cases', 'NORMAL','Normal cases','TUBER','VIRAL']
    
    for label, class_name in enumerate(class_labels):
        class_path = os.path.join(dataset_path, class_name)
        for image_name in os.listdir(class_path):
            image_path = os.path.join(class_path, image_name)
            # Add error handling for image loading
            try:
                image = Image.open(image_path)
                image = np.array(image)  # Convert PIL image to numpy array
                if image is None:
                    print(f"Error: Unable to load image '{image_path}'")
                    continue
                images.append(image)
                labels.append(label)
            except Exception as e:
                print(f"Error: {e}")
    
    # Convert lists to numpy arrays
    images = np.array(images)
    labels = np.array(labels)
    
    return images, labels

# Load test data and labels from the training directory
test_data, test_labels = load_data(r'D:\Adarsh_Jin\mds_final\medical_delivery_system\medical_delivery_system\train')

print("Test data shape:", test_data.shape)
print("Test labels shape:", test_labels.shape)

# Make predictions
predictions = model.predict(test_data)
# Convert predictions to classes
predicted_classes = np.argmax(predictions, axis=1)

# Calculate confusion matrix
conf_matrix = confusion_matrix(test_labels, predicted_classes)
print("Confusion Matrix:")
print(conf_matrix)

# Calculate accuracy
accuracy = accuracy_score(test_labels, predicted_classes)
print("Accuracy:", accuracy)

# Calculate precision
precision = precision_score(test_labels, predicted_classes, average='weighted')
print("Precision:", precision)

# Calculate recall
recall = recall_score(test_labels, predicted_classes, average='weighted')
print("Recall:", recall)

# Calculate F1 score
f1 = f1_score(test_labels, predicted_classes, average='weighted')
print("F1 Score:", f1)
