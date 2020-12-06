import cv2
import os
from PIL import Image
import numpy as np
import pickle
import shutil
# import keras

# def faceTrain():

destination = os.path.join(os.path.dirname(os.path.abspath(__file__)),'suspect_images')
Base_dir = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],'media')

# print(os.listdir(Base_dir))
for i in os.listdir(Base_dir):
    if i.endswith("png") or i.endswith("jpg") or i.endswith("jpeg"):
        try:
            os.mkdir(os.path.join(destination, i.split('_')[0]))
        except:
            pass
        shutil.move(os.path.join(Base_dir, i), os.path.join(destination, i.split('_')[0]))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, 'suspect_images')


face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            # print(label, path)
            y_labels.append(label)  # some number
            x_train.append(path)   # verify this image, trun into a numpy array


            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            # print(label_ids)


            pil_image = Image.open(path).convert("L") #gray scale
            image_array = np.array(pil_image, "uint8")
            # print(image_array)

            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
            print(faces)

            for (x,y,w,h) in faces:
                # print(roi)
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

# # print(x_train)
# # print(y_labels)

with open("labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)


recognizer.x_train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")