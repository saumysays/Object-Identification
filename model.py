"""
Using the various open-cv resources and other python libraries for model training.
"""

# importing all the required libraries. 
from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
import PIL

# Defining the Model class
class Model:

    def __init__(self):
        self.model = LinearSVC()
        
    # defining the train model method for the model
    def train_model(self, counters):
        img_list = np.array([])
        class_list = np.array([])

        for j in range(0, len(counters)):
            for i in range(1, counters[j]):
                img = cv.imread(f'{j+1}/frame{i}.jpg')[:, :, 0]
                img = img.reshape(16950)
                img_list = np.append(img_list, [img])
                class_list = np.append(class_list, j+1)
        img_list = img_list.reshape(sum(counters) -1*len(counters) , 16950)
        self.model.fit(img_list, class_list)
        print("Model successfully trained!")
    
    # the predict method that uses all the resources to print the desired result .
    def predict(self, frame):
        frame = frame[1]
        cv.imwrite("frame.jpg", cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open("frame.jpg")
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save("frame.jpg")

        img = cv.imread('frame.jpg')[:, :, 0]
        img = img.reshape(16950)
        prediction = self.model.predict([img])

        return prediction[0]
