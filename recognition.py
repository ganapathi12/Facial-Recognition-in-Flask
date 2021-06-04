import numpy as np
import cv2 #4.2.0
import os
import matplotlib.pyplot as plt
import glob
import imageio


import pkg_resources
installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])

is_installed = False
for installation in installed_packages_list:
    package, version = installation.split("==")
    
    if 'opencv-contrib-python' == package:
        is_installed = True
        break

if is_installed != True:
    raise ValueError("opencv-contrib-python is not installed on your environment. Please run pip install --user opencv-contrib-python command.")
    
opencv_home = cv2.__file__
folders = opencv_home.split(os.path.sep)[0:-1]
path = folders[0]
for folder in folders[1:]:
    path = path + "/" + folder

face_detector_path = path+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(face_detector_path);

model = cv2.face.LBPHFaceRecognizer_create() #Local Binary Patterns Histograms
#model = cv2.face.EigenFaceRecognizer_create()
#model = cv2.face.FisherFaceRecognizer_create()

def detect_face(img_path):
    img = cv2.imread(img_path)
    
    detected_faces = faceCascade.detectMultiScale(img, 1.3, 5)
    x, y, w, h = detected_faces[0] #focus on the 1st face in the image
    
    img = img[y:y+h, x:x+w] #focus on the detected area
    img = cv2.resize(img, (224, 224))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    return img

face_db=[]

def train():
    print("hi")
    global face_db
    face_db = glob.glob('test*.jpeg')
    faces = []
    for img_path in face_db:  
        #print(img_path)
        img = detect_face(img_path)
        faces.append(img)
    
    ids = np.array([i for i in range(0, len(faces))])
    pre_built_model = "pre-built-model.yml"
    
    model.train(faces, ids)
    model.save(pre_built_model)
    


def findFace(target_file):
    print("entered find face")
    images=[]
    
    img = detect_face(target_file)
    #print(img.shape)
    
    idx, confidence = model.predict(img)
    
    fig = plt.figure()

    ax1 = fig.add_subplot(1,2,1)
    #plt.imshow(img[:,:,::-1])
    plt.imshow(cv2.imread(target_file)[:,:,::-1])
    plt.axis('off')

    ax1 = fig.add_subplot(1,2,2)
    #plt.imshow(faces[id], cmap='gray')
    plt.imshow(cv2.imread(face_db[idx])[:,:,::-1])
    plt.axis('off')
    plt.savefig("resultimages.png")
    images.append(imageio.imread("resultimages.png"))
    imageio.mimsave("originalgif.gif",images)
    
    
    print("Confidence: ", round(confidence, 2))
    return confidence
    

def result():
    print("entered result")
    resultdb=glob.glob('sample*.jpeg')
    print(resultdb)
    confidence=0
    for img in resultdb:
        confidence=findFace(img)
    return confidence
    
    
    
