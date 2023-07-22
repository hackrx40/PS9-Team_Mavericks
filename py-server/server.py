from distutils.log import debug
from fileinput import filename
import cv2
from flask import *
import sys
import keras
import os 
import tensorflow as tf
from flask_socketio import SocketIO
import win32com.client

# creates a Flask application
app = Flask(__name__)
fileToWork = None
worklogs = "RUNNING CHECKS ..."
UPLOAD_FOLDER = './images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

  
@app.route("/")
def main():
    return render_template('index.html')



@app.route('/checks', methods = ['POST','GET'])  
def checks():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        with open ('filename.txt', 'w') as file:  
            file.write(f.filename)
    return render_template("checks.html")
          
    


def checkModificationinPDF(path):
    creation_time = int(os.path.getctime(path))
    modification_time = int(os.path.getmtime(path))
    return "Passed" if (creation_time <= modification_time) else "Tampering has been done in the document"
         
def checkSign(filename):
    model = tf.keras.models.load_model('./ml-sign/keras_model.h5')   
    image = cv2.imread(filename)
    image = cv2.resize(image, (224, 224))
    image = image.astype('float32') / 255.0
    image = tf.expand_dims(image, axis=0)
    results = model.predict(image)
    if results[0][0] < 1:
        result = "Tampering Detected in signature, further investigation required"
        return result
    else:
        return "Passed"
             
def checkStamp(filename):
    model = tf.keras.models.load_model('./ml-stamp/keras_model.h5')   
    image = cv2.imread(filename)
    image = cv2.resize(image, (224, 224))
    image = image.astype('float32') / 255.0
    image = tf.expand_dims(image, axis=0)
    results = model.predict(image)
    if results[0][0] < 1:
        result = "Tampering Detected in stamp, further investigation required"
        return result
    else:
        return "Passed"

@socketio.on('message')
def runTests(data):
    print('received message: ' + str(data))
    print(open("filename.txt", "r").read())
    socketio.emit('status', {
        "current":0,
        "done":1,
        "response": checkModificationinPDF(open("filename.txt", "r").read()),
    })
    
    socketio.emit('status', {
        "current":1,
        "done":2,
        "response": checkSign(open("filename.txt", "r").read()),
    })
    
    socketio.emit('status', {
        "current":2,
        "done":3,
        "response": checkStamp(open("filename.txt", "r").read()),
    })
    
    
    ##delete the file name and file after all the text has been done
    os.remove(open("filename.txt", "r").read())
    os.remove('filename.txt')
    
    
# run the application
if __name__ == "__main__":
    socketio.run(app)