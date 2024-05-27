
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

cannyThreshold = 50
cannyThresholdLinking = 150
thresholdValue = 128

current_image = None

def update_canny_threshold(value):
    global cannyThreshold
    cannyThreshold = int(value)
    if current_image is not None:
        display_image(current_image)

def update_canny_link_threshold(value):
    global cannyThresholdLinking
    cannyThresholdLinking = int(value)
    if current_image is not None:
        display_image(current_image)

def update_threshold_value(value):
    global thresholdValue
    thresholdValue = int(value)
    if current_image is not None:
        display_image(current_image)

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        process_image(file_path)

def open_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        process_video(file_path)

def start_webcam():
    process_video(0)

def process_image(file_path):
    global current_image
    img = cv2.imread(file_path)
    if img is not None:
        current_image = img
        display_image(img)

def process_video(source):
    global current_image
    current_image = None
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Error: Could not open video source.")
        return

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return
        display_image(frame)
        root.after(10, update_frame)

    update_frame()

def display_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, cannyThreshold, cannyThresholdLinking)
    _, thresh = cv2.threshold(gray, thresholdValue, 255, cv2.THRESH_BINARY)

    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    thresh_rgb = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    combined = np.hstack((edges_rgb, thresh_rgb))
    combined = cv2.resize(combined, (800, 400))

    img = Image.fromarray(combined)
    imgtk = ImageTk.PhotoImage(image=img)
    display_label.imgtk = imgtk
    display_label.configure(image=imgtk)

root = tk.Tk()
root.title("Video Filter Application")

display_label = tk.Label(root)
display_label.pack()

button_frame = tk.Frame(root)
button_frame.pack()

open_image_button = tk.Button(button_frame, text="Open Image", command=open_image)
open_image_button.grid(row=0, column=0)

open_video_button = tk.Button(button_frame, text="Open Video", command=open_video)
open_video_button.grid(row=0, column=1)

webcam_button = tk.Button(button_frame, text="Start Webcam", command=start_webcam)
webcam_button.grid(row=0, column=2)

slider_frame = tk.Frame(root)
slider_frame.pack()

canny_slider = tk.Scale(slider_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Canny Threshold", command=update_canny_threshold)
canny_slider.set(cannyThreshold)
canny_slider.pack()

canny_link_slider = tk.Scale(slider_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Canny Linking", command=update_canny_link_threshold)
canny_link_slider.set(cannyThresholdLinking)
canny_link_slider.pack()

threshold_slider = tk.Scale(slider_frame, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold", command=update_threshold_value)
threshold_slider.set(thresholdValue)
threshold_slider.pack()

root.mainloop()

