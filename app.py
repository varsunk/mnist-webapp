from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from inference import make_prediction
import os

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# creating an instance directory
# os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# store and display uploaded image
@app.route('/', methods=['POST'])
def image_upload():
    img = request.files['file']
    img_filename = secure_filename(img.filename)
    img_path = os.path.join(UPLOAD_FOLDER, img_filename)
    img.save(img_path)

    # make prediction here
    prediction = make_prediction(img_path)
    # print(f'Prediction = {prediction}')

    return render_template('index.html', filename=img_filename, prediction=prediction)

@app.route('/<filename>')
def image_display(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug = True)