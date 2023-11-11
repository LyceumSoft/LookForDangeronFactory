import torch
torch.cuda.is_available()
torch.cuda.get_device_properties(0).name

'''
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
results = model.train(data='data.yaml', epochs=100, imgsz=640, device="gpu")
'''