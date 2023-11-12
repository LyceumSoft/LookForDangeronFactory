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
pass_to_save = 'C:/Users/Admin/Desktop/idol_yolo/runs/detect/train13/1.jpg' 

photo_pass = input('Введите путь до фото: ')
save_path = 'C:/Users/Admin/Desktop/train_dataset_train_1/pic_posle_save' #путь куда сохранится фото
name_save = 'yolo_posle' #название сохраненой картинки
model = YOLO("C:/Users/Admin/esktop/Object-Detection-101/Yolo-Weights/people_in_zavod.pt") # наша добученая модель


csv_out = ''

#--доп списки для работы--#
pod_mass = []
people_cord = [] 
img_name = []
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

zone_name = ['DpR-Csp-uipv-ShV-V1', 'Pgp-com2-K-1-0-9-36', 'Pgp-lpc2-K-0-1-38', 'Phl-com3-Shv2-9-K34', 'Php-Angc-K3-1', 'Php-Angc-K3-8', 'Php-Ctm-K-1-12-56', 
             'Php-Ctm-Shv1-2-K3', 'Php-nta4-shv016309-k2-1-7', 'Spp-210-K1-3-3-5', 'Spp-210-K1-3-3-6', 'Spp-K1-1-2-6']
video_pass = r'C:\Users\Admin\Desktop\test_dataset_test_xak\videos\DpR-Csp-uipv-ShV-V1'

area_points_mass = [[(534, 288), (834, 219), (1365, 580), (1124, 806)], 
                    [(511, 214), (776, 265), (788, 367), (445, 720), (225, 717), (195, 597), (591, 315), (468, 265)],
                    [(181, 321), (378, 310), (379, 360), (553, 334), (544, 274), (907, 227), (996, 363), (895, 390), (881, 435), (582, 491), (570, 435), (375, 459), (371, 541), (170, 551)],
                    [(1335, 640), (1505, 662), (1491, 776), (1290, 752)], 
                    [(471, 717), (1434, 737), (1460, 894), (1224, 896), (1223, 761), (692, 754), (680, 916), (444, 906)],
                    [(1036, 831), (480, 475), (614, 421), (1171, 691)],
                    [(516, 261), (1344, 580),  (452, 1078), (84, 352)], 
                    [(172, 1080), (115, 745), (441, 669), (422, 540), (864, 421), (864, 259), (1363, 151), (1881, 421), (1593, 529), (1824, 723), (1094, 1080)],
                    [(0, 1080), (0, 712), (192, 518), (384, 518), (825, 97), (902, 97), (1132, 367), (1132, 583), (1555, 572), (1574, 475), (1920, 475), (1920, 1080)],
                    [(718, 204), (1128, 340), (1128, 720), (541, 720), (345, 607)],
                    [(223, 345), (639, 193), (951, 477), (494, 707)],
                    [(930, 142), (1030, 320), (946, 333), (876, 157)], 
                    ] #точки опасных зон


zoner = '' # переменая отвечающая за определние камеры



def draw_zone(image, points):
    overlay = image.copy()
    output = image.copy()
    zone_color = (255, 100, 0)  
    thickness = 2  
    for i in range(len(points) - 1):
        cv2.line(overlay, points[i], points[i + 1], zone_color, thickness)
    cv2.fillPoly(overlay, [np.array(points)], zone_color)
    cv2.addWeighted(overlay, 0.5, output, 1 - 0.5, 0, output)
    return output



for i in range(len(zone_name)):
    if zone_name[i] in photo_pass:
        print(zone_name)
        area_points = area_points_mass[i]
        zoner = zone_name[i]
    
    
    
    for filename in os.listdir(video_pass):
        csv_out = f'{zone_name[0]},"{filename}",'
        if filename.endswith(".jpg"):
            photo_pass = os.path.join(video_pass, filename)
            print(filename)
            #print(photo_pass)
            photo_pass = photo_pass.replace('\\', '/')
            photo_pass = photo_pass.replace('//', '/')
            print(photo_pass)
        for i in range(len(zone_name)):
            if zone_name[i] in photo_pass:
                area_points = area_points_mass[i]
                zoner = zone_name[i]
        for i in range(1):
        
        

            pass_to_save = 'C:/Users/Admin/Desktop/idol_yolo/runs/detect/train13/1.jpg' 
            cap = cv2.VideoCapture(photo_pass)

            myColor = (0, 0, 255)
            pod_mass = []
            people_cord = []

            while True:
                success, img = cap.read()
                results = model(img, stream=True)

                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        cls = int(box.cls[0])
                        currentClass = classNames[cls]
                        if currentClass == 'person':

                        # рисование ббоксика
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            pod_mass.append(x1), pod_mass.append(y1), pod_mass.append(x2), pod_mass.append(y2)
                            people_cord.append(pod_mass)
                            pod_mass = []
                            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),1)
                            w, h = x2 - x1, y2 - y1
                            
                            cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 1)
                            cvzone.cornerRect(img, (x1, y1, w, h))
                        else:
                            break
                        pod_mass = []  
                cv2.imwrite(pass_to_save, img)
                cv2.waitKey(1)
                break
            if zoner == 'Spp-K1-1-2-6':
                mass_procent = []

                area_points_massik = [[(18, 520), (10, 398), (126, 290), (222, 341)], [(273, 286), (198, 244), (395, 103), (453, 127)], [(877, 156), (928, 142), (1029, 320), (946, 332)], [(972, 434), (1077, 414), (1245, 682), (1046, 683)]]
                for k in range(4):
                    image = cv2.imread(pass_to_save)
                    points = np.array(area_points_massik[k])
                    image_with_zone = draw_zone(image, points)
                    cv2.imwrite(pass_to_save, image_with_zone) 
                    print(pass_to_save)
                    for  jk in range(len(people_cord)):
                        if k == 0:
                            mass_procent.append(0)

                        obj_points = [Point(people_cord[jk][0], people_cord[jk][1]), Point(people_cord[jk][0], people_cord[jk][3]), Point(people_cord[jk][2], people_cord[jk][3]), Point(people_cord[jk][2], people_cord[jk][1])]
                        obj_polygon = Polygon(obj_points)
                        area_polygon = Polygon(area_points_massik[k])
                    
                        intersection_area = obj_polygon.intersection(area_polygon).area
                        obj_area = obj_polygon.area
                        percentage_inside = (intersection_area / obj_area) * 100
                        percentage_inside = round(percentage_inside, 3)
                        if percentage_inside > mass_procent[jk]:
                            mass_procent[jk] = percentage_inside
                        if percentage_inside > 15.0:
                            intersection_area = obj_polygon.intersection(area_polygon).area
                            obj_area = obj_polygon.area

                for r in range(len(mass_procent)):
                    if mass_procent[r] < 15.0:
                        
                        print(f'{csv_out}"False","{mass_procent[r]}"')
                    else:
                        print(f'{csv_out}"True","{mass_procent[r]}"')
            
            else:
                for  j in range(len(people_cord)):
                    obj_points = [Point(people_cord[j][0], people_cord[j][1]), Point(people_cord[j][0], people_cord[j][3]), Point(people_cord[j][2], people_cord[j][3]), Point(people_cord[j][2], people_cord[j][1])]
                    area_polygon = Polygon(area_points)
                    obj_polygon = Polygon(obj_points)
                    intersection_area = obj_polygon.intersection(area_polygon).area
                    obj_area = obj_polygon.area
                    percentage_inside = (intersection_area / obj_area) * 100
                    percentage_inside = round(percentage_inside, 3)
                    # Проверяем вхождение объекта в область
                    if percentage_inside > 15.0:
                        intersection_area = obj_polygon.intersection(area_polygon).area
                        obj_area = obj_polygon.area
                        print(f'{csv_out}"True","{percentage_inside}"')
                    elif people_cord == []:
                        print(f'{csv_out}"False","{percentage_inside}"')

                    else:
                        print(f'{csv_out}"False","{percentage_inside}"')
        photo_pass = ''
image = cv2.imread(pass_to_save)
points = np.array(area_points)
image_with_zone = draw_zone(image, points)
cv2.imwrite(pass_to_save, image_with_zone) 
print(pass_to_save)
