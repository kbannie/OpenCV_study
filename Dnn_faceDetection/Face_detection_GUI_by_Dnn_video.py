import cv2
import numpy as np
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog


model_name='./Data/res10_300x300_ssd_iter_140000.caffemodel'
prototxt_name='./Data/deploy.prototxt.txt' #아키텍처 구성도
min_confidence=0.5 #50% 이상 확률만 보여주기
file_name = './Data/video/obama_01.mp4'
title_name = 'dnn Deep Learnig object detection Video'
frame_width = 300
frame_height = 300
cap = cv2.VideoCapture()

def selectFile():
    file_name =  filedialog.askopenfilename(initialdir = "./video",title = "Select file",filetypes = (("MP4 files","*.mp4"),("all files","*.*")))
    print('File name : ', file_name)
    global cap
    cap = cv2.VideoCapture(file_name)
    detectAndDisplay()
    
def detectAndDisplay():
    #자체적으로 재귀함수처럼 돌아오기
    _, frame = cap.read()
    (h, w) = frame.shape[:2] 
    model = cv2.dnn.readNetFromCaffe(prototxt_name, model_name)

    # Resizing to a fixed 300x300 pixels and then normalizing it
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))

    model.setInput(blob)
    detections = model.forward()

    min_confidence = float(sizeSpin.get())
    
    # loop over the detections
    for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > min_confidence:
                    (height, width) = frame.shape[:2]
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
     

                    text = "{:.2f}%".format(confidence * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                            (0, 255, 0), 2)
                    cv2.putText(frame, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, detectAndDisplay) 
    
    
#main
main = Tk()
main.title(title_name)
main.geometry()

#Graphics window
label=Label(main, text=title_name)
label.config(font=("Courier", 18))
label.grid(row=0,column=0,columnspan=4)
sizeLabel=Label(main, text='Min Confidence : ')
sizeLabel.grid(row=1,column=0)
sizeVal  = IntVar(value=min_confidence)
sizeSpin = Spinbox(main, textvariable=sizeVal,from_=0, to=1, increment=0.05, justify=RIGHT)
sizeSpin.grid(row=1, column=1)

Button(main,text="File Select", height=2,command=lambda:selectFile()).grid(row=1, column=2, columnspan=2, sticky=(W, E))
imageFrame = Frame(main)
imageFrame.grid(row=2,column=0,columnspan=4)
  
#Capture video frames
lmain = Label(imageFrame)
lmain.grid(row=0, column=0)

main.mainloop()  #Starts GUI
