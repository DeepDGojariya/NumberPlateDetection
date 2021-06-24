from flask import Flask,render_template,request,flash,url_for,redirect,send_from_directory,config
from werkzeug.utils import secure_filename
import os
from util import single_image_pred

MEDIA_FOLDER = 'upload'
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
IMAGE_NAME_=''
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(MEDIA_FOLDER, filename, as_attachment=True)


@app.route('/',methods=['GET','POST'])
def index():
    global IMAGE_NAME_
    if request.method=='POST':
        file = request.files['userfile']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        IMAGE_NAME_ = filename
        return render_template("index.html",context={"id":1,"name":filename})
    return render_template("index.html",context={"id":2})

@app.route('/predictions',methods=['POST'])
def predict():
    global IMAGE_NAME_
    if request.method=='POST':
        text = single_image_pred(IMAGE_NAME_)
    return render_template("predict.html",context={'name':'current.png','plate':text})

@app.route('/about')
def about():
    return render_template('about.html')
if __name__=="__main__":
    app.run(debug=True)


