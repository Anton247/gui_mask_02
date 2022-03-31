# Пример захвата изображения с камеры на аппарате MiddleAUV.
# Имейте ввиду, что возможность вывода видеопотока в MUR IDE
# с помощью auv.get_videoserver доступна лишь в достаточно
# новых аппаратах (MiddleAUV, произведённые с мая 2021 года)

from time import sleep
from datetime import datetime
import cv2
#from imutils.video import VideoStream

import numpy as np
import socket
import sys
import pickle
import struct
import time
from PIL import Image

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 7777))


cap = cv2.VideoCapture(0)

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

font = cv2.FONT_HERSHEY_DUPLEX

while True:
    ok, img = cap.read()
    
    if ok: # Если кадр успешно прочитан
        image = img.copy()
        image = image.resize((1366, 768))
        image = np.array(image)
        img = Image.frombytes('RGB', (1366, 768), image)
        data = pickle.dumps(np.array(img))
        clientsocket.sendall(struct.pack("L", len(data)) + data)

    else: # При ошибке чтения кадра.
        print('camera read error')
        break

cap.release()
print("done")