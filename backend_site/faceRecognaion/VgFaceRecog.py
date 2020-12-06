import matplotlib.pyplot as plt 
from PIL import Image
from numpy import asarray
import numpy as np
from scipy.spatial.distance import cosine
from mtcnn.mtcnn import MTCNN
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import cv2

model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')
 
# determine if a candidate face is a match for a known face
def is_match(known_embedding, candidate_embedding, thresh=0.5):
	# calculate distance between embeddings
	score = cosine(known_embedding, candidate_embedding)
	if score <= thresh:
		# print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
		return True
	else:
		# print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
		return False


def recognize_face(frame, required_size=(224, 224)):
	detector = MTCNN()
	results = detector.detect_faces(frame)
	# print(results[0])

	# try:
	samples = []
	for faces in results:
		x1, y1, width, height = faces['box']
		x2, y2 = x1 + width, y1 + height
		# extract the face
		face = frame[y1:y2, x1:x2]
		# resize pixels to the model size
		image = Image.fromarray(face)
		image = image.resize(required_size)
		face_array = asarray(image)

		sample = asarray(face_array, 'float32')
		samples.append(preprocess_input(sample, version=2))

	yhat = []
	for f in samples:
		yhat.append(model.predict(np.expand_dims(f, axis=0)))
		
	return yhat
	# except:
	# 	pass



# imgs = ['images/harington/1.jpg', '1.jpg', 'images/peter/3.jpg']
# f = []
# for i in imgs:
# 	f.append(RecognizeFace(plt.imread(i)))

img = recognize_face(plt.imread('1.jpg'))
print(img[0][0])
print('length: ',len(np.array(img[0][0]).tostring()))
# print(np.array(img).shape())


def startRecog():
		
	cap = cv2.VideoCapture(0)

	while(True):
		ret, frame = cap.read()

		detection = recognize_face(frame)
		
		try:
			if len(detection) > 1:
				# print("Multi face Working")
				for d in detection:
					for suspect in f:
						if is_match(suspect, d) == True:
							print("Face Match")
							
			else:
				for suspect in f:
					if is_match(suspect, detection[0]) == True:
						print("Face Match")
		except:
			pass

		cv2.imshow('frame', frame)

		if cv2.waitKey(20) & 0xFF == ord('q'):
			break

	cap.release()
	cap.destroyAllWindow()