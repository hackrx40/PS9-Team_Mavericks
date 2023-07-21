from google.cloud import vision
from flask import render_template
from distutils.log import debug
from fileinput import filename
from flask import *
import pikepdf
import sys


# creates a Flask application
app = Flask(__name__)
fileToWork = None
worklogs = "RUNNING CHECKS ..."
  
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        return render_template("Acknowledgement.html", name = f.filename, logs=runchecks(f.filename)) 
          


def runchecks(fileToWork) :
    checkModificationinPDF(fileToWork)
    
    
def checkModificationinPDF(pdf_filename):
    pdf = pikepdf.Pdf.open(pdf_filename)
    docinfo = pdf.docinfo
    print(docinfo["/ModDate"]==docinfo["/CreationDate"])
         
def detect_properties(path):
    """Detects image properties in the file."""
    

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    print("Properties:")

    for color in props.dominant_colors.colors:
        print(f"fraction: {color.pixel_fraction}")
        print(f"\tr: {color.color.red}")
        print(f"\tg: {color.color.green}")
        print(f"\tb: {color.color.blue}")
        print(f"\ta: {color.color.alpha}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
        
        
        
    


# run the application
if __name__ == "__main__":
    app.run(debug=True)