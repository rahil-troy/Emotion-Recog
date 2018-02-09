# Proof-of-concept
import cv2
import sys
from constants import *
from emotion_recognition import EmotionRecognition
import numpy as np

path = "/home/troy-rahil/repo/emotion-recognition-neural-networks/haarcascade_files/haarcascade_frontalface_default.xml"
#EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']
EMOTIONS = ['angry','happy','neutral']
cascade_classifier = cv2.CascadeClassifier(path)

def brighten(data,b):
     datab = data * b
     return datab    

def format_image(image):
  if len(image.shape) > 2 and image.shape[2] == 3:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  else:
    image = cv2.imdecode(image, cv2.CV_LOAD_IMAGE_GRAYSCALE)
  faces = cascade_classifier.detectMultiScale(
      image,
      scaleFactor = 1.3,
      minNeighbors = 5
  )
  # None is we don't found an image
  if not len(faces) > 0:
    return None
  max_area_face = faces[0]
  for face in faces:
    if face[2] * face[3] > max_area_face[2] * max_area_face[3]:
      max_area_face = face
  # Chop image to face
  face = max_area_face
  image = image[face[1]:(face[1] + face[2]), face[0]:(face[0] + face[3])]
  # Resize image to network size
  try:
    image = cv2.resize(image, (SIZE_FACE, SIZE_FACE), interpolation = cv2.INTER_CUBIC) / 255.
  except Exception:
    print("[+] Problem during resize")
    return None
  # cv2.imshow("Lol", image)
  # cv2.waitKey(0)
  return image

# Load Model
network = EmotionRecognition()
network.build_network()

video_capture = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

feelings_faces = []
for ind, emotion in enumerate(EMOTIONS):
  feelings_faces.append(cv2.imread('/home/troy-rahil/repo/emotion-recognition-neural-networks/emojis' + emotion + '.png', -1))

while True:
  # Capture frame-by-frame
  ret, frame = video_capture.read()

  # Predict result with network
  result = network.predict(format_image(frame))
  if result is not None:
  	print max(result[0])
  # Draw face in frame
  # for (x,y,w,h) in faces:
  #   cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)

  # Write results in frame
  '''if result is not None:
    for ind, emotion in enumerate(EMOTIONS):
      cv2.putText(frame, emotion, (10, ind * 20 + 20), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1);
      cv2.rectangle(frame, (130, ind * 20 + 10), (130 + int(result[0][ind] * 100), (ind + 1) * 20 + 4), (255, 0, 0), -1)
  
    print(type(result))
    print(feelings_faces)
    face_image = feelings_faces[result[0].tolist().index(max(result[0]))]
    # Ugly transparent fix
    print(type(face_image))
    for c in range(0, 3):
      frame[200:320, 10:130, c] = face_image[:,:,c] * (face_image[:, :, 3] / 255.0) +  frame[200:320, 10:130, c] * (1.0 - face_image[:, :, 3] / 255.0)
      '''
  # Display the resulting frame
  cv2.imshow('Video', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()