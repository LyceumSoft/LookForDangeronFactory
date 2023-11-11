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
def read_logs():
    static_folder = os.path.join(app.root_path, "static")
    with open(f"{static_folder}/logs.txt", "r", encoding="utf-8") as file:
        log_lines = file.readlines()
    return log_lines

def get_video_files():
    static_folder = os.path.join(app.root_path, "static")
    video_files = [f for f in os.listdir(static_folder) if f.endswith(".jpg")]
    return video_files

def generate_img():
    video_files = get_video_files()

def generate_image_path(button_text):
    txt = button_text + ".jpg"
    return txt

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

@app.route('/test', methods=['GET'])
def test(): 
    text = request.args.get('text')
    print(text)
    return "true"

@app.route('/')
def home(): 
    return render_template('main.html')

@app.route('/get_log_lines', methods=['GET'])
def get_log_lines():
    print("logsupd")
    data = read_logs()
    print(data)
    return jsonify({"log_lines": data})
    
@app.route('/cameras', methods=['POST'])
def cameras():
    return render_template('cameras.html')

@app.route('/logs', methods=['POST'])
def logs(): 
    log_lines = read_logs()
    return render_template('logs.html', log_lines=log_lines)

if __name__ == '__main__':
    app.run()
    print("off")
