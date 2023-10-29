"""
This is the main part of the Project , where all the major parts of project are defined 
"""
# importing all the required libraries {open-sourced and built-in}
import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import os
import PIL.Image, PIL.ImageTk
import model
import camera

# defining the Class Application where all the main part of the project is defined
class App:
    
# Using the constructor to define the elements for the Application Class
    def __init__(self, window=tk.Tk(), window_title="Camera Classifier"):

        self.window = window
        self.window_title = window_title

        self.model = model.Model()

        self.auto_predict = False
        self.folders = []

        self.camera = camera.Camera()

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes("-topmost", True)
        self.window.mainloop()

    # Defining the Method for Graphical User Interface
    def init_gui(self):
        
        # Creating the window using tkinter
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()
        
        # Defining all the major buttons in the UI alongside with their commands.
        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.num = simpledialog.askinteger("Object Count", "Enter the number of objects you want:", parent=self.window)
        
        # Defining all the classes and their buttons // {num of objects that are being trained can be edited}
        self.counters = []
        for i in range(self.num):
            self.counters.append(1)

        i, k = 1, self.num
        while i <= k:
            if i == 1:
                self.classname_one = simpledialog.askstring("Classname One", "Enter the name of the first class:",
                                                            parent=self.window)

                self.btn_class_one = tk.Button(self.window, text=self.classname_one, width=50,
                                               command=lambda: self.save_for_class(1))
                self.btn_class_one.pack(anchor=tk.CENTER, expand=True)

            elif i == 2:
                self.classname_two = simpledialog.askstring("Classname Two", "Enter the name of the second class:",
                                                            parent=self.window)

                self.btn_class_two = tk.Button(self.window, text=self.classname_two, width=50,
                                               command=lambda: self.save_for_class(2))
                self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

            elif i == 3:
                self.classname_three = simpledialog.askstring("Classname Third", "Enter the name of the third class:",
                                                              parent=self.window)

                self.btn_class_three = tk.Button(self.window, text=self.classname_three, width=50,
                                               command=lambda: self.save_for_class(3))
                self.btn_class_three.pack(anchor=tk.CENTER, expand=True)

            elif i == 4:
                self.classname_four = simpledialog.askstring("Classname Fourth", "Enter the name of the fourth class:",
                                                            parent=self.window)

                self.btn_class_four = tk.Button(self.window, text=self.classname_four, width=50,
                                               command=lambda: self.save_for_class(4))
                self.btn_class_four.pack(anchor=tk.CENTER, expand=True)

            elif i == 5:
                self.classname_five = simpledialog.askstring("Classname Fifth", "Enter the name of the fifth class:",
                                                            parent=self.window)

                self.btn_class_five = tk.Button(self.window, text=self.classname_five, width=50,
                                               command=lambda: self.save_for_class(5))
                self.btn_class_five.pack(anchor=tk.CENTER, expand=True)

            elif i == 6:
                self.classname_six = simpledialog.askstring("Classname Sixth", "Enter the name of the sixth class:",
                                                            parent=self.window)

                self.btn_class_six = tk.Button(self.window, text=self.classname_six, width=50,
                                               command=lambda: self.save_for_class(6))
                self.btn_class_six.pack(anchor=tk.CENTER, expand=True)

            elif i == 7:
                self.classname_seven = simpledialog.askstring("Classname Seventh", "Enter the name of the seventh class:",
                                                            parent=self.window)

                self.btn_class_seven = tk.Button(self.window, text=self.classname_seven, width=50,
                                               command=lambda: self.save_for_class(7))
                self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

            elif i == 8:
                self.classname_eight = simpledialog.askstring("Classname Eighth", "Enter the name of the eighth class:",
                                                            parent=self.window)

                self.btn_class_eight = tk.Button(self.window, text=self.classname_eight, width=50,
                                               command=lambda: self.save_for_class(8))
                self.btn_class_two.pack(anchor=tk.CENTER, expand=True)

            i += 1
            
        # Defining the Button for training model //it calls the model class for training the model with the data 
        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text="Predcit", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.class_label = tk.Label(self.window, text="____")
        self.class_label.config(font=("Arial", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)


    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict
        
    # Defining the Save_for_class method , which stores the input data , into sorted and different directories
    def save_for_class(self, class_num):
        ret, frame = self.camera.get_frame()
        if not os.path.exists(str(class_num)):
            os.mkdir(str(class_num))
            self.folders.append(str(class_num))

        cv.imwrite(f'{class_num}/frame{self.counters[class_num-1]}.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open(f'{class_num}/frame{self.counters[class_num - 1]}.jpg')
        img.thumbnail((150, 150), PIL.Image.ANTIALIAS)
        img.save(f'{class_num}/frame{self.counters[class_num - 1]}.jpg')

        self.counters[class_num - 1] += 1

# reset function
    def reset(self):
        for folder in self.folders:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        self.counters = []
        self.model = model.Model()
        self.class_label.config(text="____")

    # Defining the update method // to continously update the Graphical User Interface
    def update(self):
        if self.auto_predict:
            print(self.predict())

        ret, frame = self.camera.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)
        
    # Defining the predict method, that takes predictions done by the Model and displays them in the interface.
    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model.predict(frame)


        if prediction == 1:
            self.class_label.config(text=self.classname_one)
            return self.classname_one
        if prediction == 2:
            self.class_label.config(text=self.classname_two)
            return self.classname_two
        try:
            if prediction == 3:
                self.class_label.config(text=self.classname_three)
                return self.classname_three
        except:
            pass

        try:
            if prediction == 4:
                self.class_label.config(text=self.classname_four)
                return self.classname_four
        except:
            pass

        try:
            if prediction == 5:
                self.class_label.config(text=self.classname_five)
                return self.classname_five
        except:
            pass
        try:
            if prediction == 6:
                self.class_label.config(text=self.classname_six)
                return self.classname_six
        except:
            pass
        try:
            if prediction == 7:
                self.class_label.config(text=self.classname_seven)
                return self.classname_seven
        except:
            pass
        try:
            if prediction == 8:
                self.class_label.config(text=self.classname_eight)
                return self.classname_eight
        except:
            pass
        
