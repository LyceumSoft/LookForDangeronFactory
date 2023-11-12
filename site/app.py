import numpy as np
import cv2
import numpy as np
from ultralytics import YOLO
import os
import cv2 as cv
import glob
from flask import Flask, render_template, jsonify, request
import PIL
import cv2
import time
import cv2
import numpy as np

from ultralytics import YOLO
import cv2
import cv2 as cv
import cvzone
import math
import time
import os
import json
from shapely.geometry import Point, Polygon
app = Flask(__name__, static_url_path="/static")

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route('/get_image_name', methods=['GET'])
def get_image_name():
    button_text = request.args.get('button_text')
    new_image_path = generate_image_path(button_text)
    print(new_image_path)
    return jsonify({"image_path": new_image_path})

@app.route('/')
def home(): 
    return render_template('main.html')
    
@app.route('/upload', methods=['POST'])
def upload():
    from roboflow import Roboflow
    target_dir = "F:\!newgit\LookForDangeronFactory\site\static\\"
    file = request.files['file']
    file.save(target_dir + file.filename)
    rf = Roboflow(api_key="6u6b1sk0YqWRx4fQPw3d")
    project = rf.workspace().project("presondetext")
    model = project.version(1).model
    prediction_result = model.predict(f"F:\!newgit\LookForDangeronFactory\site\static\\{file.filename}", confidence=40, overlap=30).json()
    print(prediction_result)
    if 'predictions' in prediction_result and len(prediction_result['predictions']) > 0:
            # Loop through all predictions
            for i, prediction in enumerate(prediction_result['predictions']):
                center_x = prediction['x']
                center_y = prediction['y']
                width = prediction['width']
                height = prediction['height']
                x1 = int(center_x - width / 2)
                y1 = int(center_y - height / 2)
                x2 = int(center_x + width / 2)
                y2 = int(center_y + height / 2)
                # Print the coordinates for each bounding box
                print(f'Bbox {i + 1} Coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}')

    model.predict(f"F:\!newgit\LookForDangeronFactory\site\static\\{file.filename}", confidence=40, overlap=30).save("F:\!newgit\LookForDangeronFactory\site\static\predicted_" + file.filename)
    
    image_path =  "predicted_" + file.filename
    return render_template('upload.html', image_path=image_path)

if __name__ == '__main__':
    app.run()
    print("off")
