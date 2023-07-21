
from flask import render_template
from distutils.log import debug
from fileinput import filename
from flask import * 
  
# creates a Flask application
app = Flask(__name__)
fileToWork = None
  
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)
        fileToWork = f
        return render_template("Acknowledgement.html", name = f.filename) 
          
# run the application
if __name__ == "__main__":
    app.run(debug=True)