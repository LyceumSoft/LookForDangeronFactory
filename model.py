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
video_path = './vids/Камера1.mp4' # путь к видео
save_path = './site/static' # куда сохранится кадр на котором пользователь выделял
coord_path = './site/static/cords.txt' # путь к ткстшнику куда сохрантся корды

#-----ЧИСЛА-----№

tochnost = 0.4 # ТОЧНОСТЬ РАСПОЗНОВАНИЕ ЧЕЛОВЕКА ЕЛКОЙ
count_pluser = 80 # КОЛВО ПИКСЕЛЕЙ ДЛЯ ДОП ББОКСИКА(ЖЕЛТАЯ ЗОНА)

model = YOLO("./yolov8n.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
matrix_bbox = []
#matrix_bbox = [[371, 289, 193, 649], [691, 384, 940, 174]] - можно юзать для тестов если нету ввода в консоль

# ФУНКЦИЯ ДЛЯ СЧИТЫВАНИЯ КООРДИНАТ
def while_input():
    bbox_small = []
    while True:
        a = input('Введите координату(x1) или поставьте Enter ') 
        if a == '':
            break
        else:
            ris_x1 = int(a)
            ris_y1 = int(input('y1 '))
            ris_x2 = int(input('x2 '))
            ris_y2 = int(input('y2 '))
            bbox_small.append(ris_x1)
            bbox_small.append(ris_y1)
            bbox_small.append(ris_x2)
            bbox_small.append(ris_y2)
            matrix_bbox.append(bbox_small)
            bbox_small = []

#СООРТИРОВКА МАТРИЦЫ ЕСЛИ МАТРИЦА ВВЕДЕНА НЕ ТАК КАК НАДО
def matrix_sort(matrix_bbox):
    matrix_input = matrix_bbox
    matrix_clear = []
    matrix_output = []
    x1_ris, x2_ris, y1_ris, y2_ris = 0, 0, 0, 0,
    for i in range(len(matrix_input)):
        if matrix_input[i][0] > matrix_input[i][2]:
            x1_ris = matrix_input[i][2]
            x2_ris = matrix_input[i][0]
        else:
            x1_ris = matrix_input[i][0]
            x2_ris = matrix_input[i][2]

        if matrix_input[i][1] > matrix_input[i][3]:
            y1_ris = matrix_input[i][3]
            y2_ris = matrix_input[i][1]
        else:
            y1_ris = matrix_input[i][1]
            y2_ris = matrix_input[i][3]

        matrix_clear.append(x1_ris), matrix_clear.append(y1_ris), matrix_clear.append(x2_ris), matrix_clear.append(y2_ris)
        matrix_output.append(matrix_clear)
        matrix_clear = []
    matrix_bbox = matrix_output
    print(matrix_bbox)
    
    return matrix_bbox

def cord_save_txt(matrix_bbox):
    with open(coord_path, 'w') as fw:
    # записываем
        json.dump(matrix_bbox, fw)
def cord_import_txt(matrix_bbox):
    with open(coord_path, 'r') as fr:
    # читаем из файла
        matrix_bbox = json.load(fr)
    return matrix_bbox

#ФУНКЦИЯ ДЛЯ ББОКСОВ
def bbox_video(matrix_bbox, video_path, save_path):
    prev_frame_time = 0
    new_frame_time = 0
    frame_number = 0

    cap = cv2.VideoCapture(video_path)

    # Проверка успешности загрузки видео
    if not cap.isOpened():
        print("Ошибка при загрузке видео")
        exit()
    # Чтение первого кадра и его размеров
    ret, frame = cap.read()
    if not ret:
        print("Не удалось прочитать кадр")
        exit()
    height, width, _ = frame.shape
    
    bbox_small = []
    while True:
        frame_number = 0
        new_frame_time = time.time()
        success, img = cap.read()
        results = model(img, stream=True)
        if not success:
            break
        for r in results:
            boxes = r.boxes
            for box in boxes:
                #СОЗДАНИЕ ББОКСОВ НА ВИДЕО
                for i in range(len(matrix_bbox)):
                    cv2.rectangle(img, (matrix_bbox[i][0], matrix_bbox[i][1]), (matrix_bbox[i][2], matrix_bbox[i][3]), (255, 255, 255), 2)
                cls = int(box.cls[0])
                if classNames[cls] == "person" and math.ceil((box.conf[0] * 100)) / 100 > tochnost:

                #ВЫДЕЛЕНИЕ САМОГО ОБЪЕКТА

                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    

                #---РАБОТА-С-ОПАСНЫМИ-ЗОНАМИ---#
                    peresec = 0 #ПЕРЕМЕННЫЕ ДЛЯ РАБОТЫ ДОП ЗОН
                    peresec_2 = 0

           
                    for i in range(len(matrix_bbox)):
                 
                        if (matrix_bbox[i][0] < x1 < matrix_bbox[i][2] or matrix_bbox[i][0] < x2 < matrix_bbox[i][2]) and (matrix_bbox[i][1] < y1 < matrix_bbox[i][3] or matrix_bbox[i][1] < y2 < matrix_bbox[i][3]):
                            peresec += 1
                      
                        elif (matrix_bbox[i][0] - count_pluser < x1 < matrix_bbox[i][2] + count_pluser or matrix_bbox[i][0] - count_pluser < x2 < matrix_bbox[i][2] + count_pluser) and (matrix_bbox[i][1] - count_pluser < y1 < matrix_bbox[i][3] + count_pluser or matrix_bbox[i][1] - count_pluser < y2 < matrix_bbox[i][3] + count_pluser):
                            peresec_2 += 1

            #---РАБОТА-С-ББОКСИКОМ-ЧЕЛОВЕКА---#
                    # ЗЕЛЕНЫЙ ЦВЕТ ББОКСИКА  
                    if peresec >= 1:
                        cv2.rectangle(img,(x1,y1),(x2,y2), (0, 0, 255),3)
                    # ЖЕЛТЫЙ ЦВЕТ ББОКСИКА
                    elif peresec_2 >= 1:
                        cv2.rectangle(img,(x1,y1),(x2,y2), (0, 80, 120),3)
                    #КРАСНЫЙ ЦВЕТ ББОКСИКА
                    else:
                        cv2.rectangle(img,(x1,y1),(x2,y2), (0, 150, 50),3)

            #---РИСОВАНИЕ-КЛАССА-И-ТОЧНОСТИ---#
                
                # ТОЧНОСТЬ ВЫДЕЛЕННОГО ОБЪЕКТА (ДЛЯ ВЫВОДА НА ВИДЕО)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                # СОЗДАНИЕ КВАДРАТИКА С ТОЧНОСТЬЮ И НАЗВАНИЕМ КЛАССА
                    
                    cvzone.putTextRect(img, f'', (max(0, x1), max(35, y1)), scale=1, thickness=0) # РИСУЕТ НАЗВАНИЕ КЛАССА НАД ББОКСОМ
    
                    # Сохранение кадра в папку
                   
    #---FPS-НА-ВИДЕО---#
     
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        print(fps)
        if success:      
            video_name = video_path.split('/')[-1].split('.')[0]
            frame_name = f"{video_name}.jpg"  # Имя файла будет одинаковым при каждой итерации
            frame_path = os.path.join(save_path, frame_name)
            cv2.imwrite(frame_path, img)
            frame_number += 1
            
matrix_bbox = matrix_sort(matrix_bbox)
cord_save_txt(matrix_bbox)
matrix_bbox = cord_import_txt(matrix_bbox)
bbox_video(matrix_bbox, video_path, save_path)