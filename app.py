from flask import Flask, send_file, url_for,render_template, flash, request, redirect
from flask import *  
#import graphs
import recognition
import os
import time
#from mako.template import Template

app = Flask(__name__)
app.secret_key = "abc"  

ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['POST','GET'])
def page0():
    
    
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
    recognition.train()
    return render_template('index.html')

@app.route('/registering', methods = ['POST','GET'])
def takingimage():
    #if request.method == 'POST':  
     #   f = request.files['file']  
      #  f.save(f.filename)  
    return render_template('takingimage.html')

@app.route('/recognising', methods = ['POST','GET'])
def recognising():
    #if request.method == 'POST':  
     #   f = request.files['file']  
      #  f.save(f.filename)  
    return render_template('recognisingimage.html')

@app.route('/result', methods = ['POST','GET'])
def result():
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename) 
    confidence=recognition.result()
    if(confidence<80):
        return send_file('originalgif.gif', mimetype='image/gif')
    else:
        return send_file('imagenotmatch.gif', mimetype='image/gif')
        

@app.route('/About')
def about():
    return render_template('about.html')



if __name__ == "__main__":
    app.run(debug=True)
    
    
