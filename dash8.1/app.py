from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app= Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')
    

@app.route('/alogin', methods=['GET', 'POST'])
def alogin():
    if request.method=='POST':
        conn=sqlite3.connect('jaxdb.db')
        cursor= conn.cursor()

        
        password= request.form['apassword']
        email= request.form['aemail']


        cursor.execute("SELECT * FROM jaxadmin WHERE username= ? AND password= ? ", (email, password))
        res= cursor.fetchone()

        #close the connection
        conn.close()

        if res:
            # Successful login
            return render_template('admindash.html')
        else:
            # Failed login
            return "Invalid username or password"

    return render_template('alogin.html')

# -------------------------------------------------------------------------------------------------------

@app.route('/dlogin', methods= ['GET', 'POST'])
def dlogin():
    if request.method=='POST':
        conn= sqlite3.connect('jaxdb.db')
        cursor=conn.cursor()

        # cursor.execute('''CREATE TABLE IF NOT EXISTS Doctor (
        #                 id INTEGER PRIMARY KEY,
        #                 name TEXT NOT NULL,
        #                 username TEXT NOT NULL,
        #                 password TEXT NOT NULL
        #             )''')
        
        # Inserting data into the database
        # cursor.execute("INSERT INTO doctor (id, name, username, password) VALUES (7098, 'Adarsh', 'adarshjin@gmail.com', 'password')")
        # conn.commit()
        # conn.close()
        password= request.form['dpassword']
        email= request.form['dmail']


        cursor.execute("SELECT * FROM jaxdoctor WHERE name= ? AND password= ? ", (email, password))
        res= cursor.fetchone()

            #close the connection
        conn.close()

        if res:
                # Successful login
                return render_template('docdash.html')
        else:
                # Failed login
                return "Invalid username or password"

        # cursor.execute("DROP TABLE IF EXISTS doctor")
    return render_template('dlogin.html')

@app.route('/admindash', methods=["POST", "GET"])
def admindash():
    if request.method=='POST':
            conn= sqlite3.connect('jaxdb.db')
            cursor=conn.cursor()

            doctor= request.form['dname']
            contact= request.form['dcontact']
            org= request.form['dhospital']
            spec= request.form['dspec']
            password=request.form['dpassword']
            
            # cursor.execute('''CREATE TABLE IF NOT EXISTS jaxdoctor (
            #                 name TEXT NOT NULL,
            #                 field TEXT NOT NULL,
            #                 hospital TEXT NOT NULL,
            #                 contact NUMERIC PRIMARY KEY NOT NULL,
            #                 password TEXT
            #             )''')


            cursor.execute("INSERT INTO jaxdoctor (name, field, hospital, contact, password) VALUES (?,?,?,?,?)", (doctor, spec, org, contact, password))
            conn.commit()
            conn.close()
    return render_template('admindash.html')
# ----------------------------------------------------------------------
from werkzeug.utils import secure_filename
from PIL import Image
import tensorflow as tf
import numpy as np
import tensorflow_addons as tfa
import numpy as np
from PIL import Image
import os

    # Define the folder where uploaded images will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
num_classes = 5 

    # Get the absolute path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'models', 'vgg_model_new.h5')

    # Define the custom metric F1Score
custom_objects = {'F1Score': tfa.metrics.F1Score(num_classes=num_classes, average='micro')}

    # Load the model with custom_objects
model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)

def preprocess_image(image_path):
        # Load the image and resize it to the required input shape
    img = Image.open(image_path).resize((224, 224))
        # Convert the image to a NumPy array
    img_array = np.array(img)
        # Ensure the image has 3 color channels (RGB)
    if img_array.shape[-1] != 3:
        img_array = np.stack([img_array] * 3, axis=-1)
        # Expand dimensions to create a batch of size 1
    img_array = np.expand_dims(img_array, axis=0)
         # Normalize pixel values to be between 0 and 1
    img_array = img_array / 255.0
    return img_array

@app.route('/imgupload', methods=["POST", "GET"])
def imageupload():
    if request.method=='POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Make sure the filename is secure to prevent any malicious activities
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Preprocess the image and perform classification using the loaded ResNet50 model
            img_array = preprocess_image(filepath)
            result = model.predict(img_array)
            class_index = np.argmax(result)
            # Map class index to label
            class_labels = ["Bacterial Pneumonia", "COVID", "Normal", "Tuberculosis", "Viral Pneumonia"]
            result_label = class_labels[class_index]
            return render_template('imgresult.html', filename=filename, result_label=result_label)
    return render_template('imgupload.html')


if __name__=="__main__":
    app.run(debug=True)
