from distutils.log import debug
from fileinput import filename
from flask import *
import sys


# creates a Flask application
app = Flask(__name__)
fileToWork = None
worklogs = "RUNNING CHECKS ..."
  
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/checks', methods = ['POST','GET'])  
def checks():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        return render_template("ack.html", name = f.filename) 
    else :

        return render_template("checks.html")
          


def runchecks(fileToWork) :
    checkSign(file)
    # checkModificationinPDF(fileToWork)
    pass
    
    
def checkModificationinPDF(pdf_filename):
    # pdf = pikepdf.Pdf.open(pdf_filename)
    # docinfo = pdf.docinfo
    # print(docinfo["/ModDate"]==docinfo["/CreationDate"])
    pass
         
def checkSign():
    


# run the application
if __name__ == "__main__":
    app.run(debug=True)