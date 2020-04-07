#import all required libraries

import random
import math
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import json
import numpy as np
from network2 import *
from misc import sigmoid
import tensorflow as tf

net = load("model.txt")
# net.biases = tf.convert_to_tensor(net.biases, dtype=tf.dtypes.float32)
# net.weights = tf.convert_to_tensor(net.weights, dtype=tf.dtypes.float32)

def predict_digit(img):
	#resize image to 28x28 pixels
    img = img.resize((28,28))

    #convert rgb to grayscale
    img = img.convert('L')
    img = np.array(img)
    # img = tf.convert_to_tensor(img, dtype = tf.float32)

    #reshaping to support our model input and normalizing
    img = np.reshape(img, (1, 784, 1))
    img = img/255.0

    t = sigm(np.dot(net.weights[0], img[0]) + net.biases[0])
    res = sigm(np.dot(net.weights[1], t) + net.biases[1])
    print(res)

    return np.argmax(res)


def predict(img):
	for x in img:
		for b,w in zip(net.biases, net.weights):
			x = [sigm(np.dot(w,x)+b)]
	print(x)
	return x

def sigm(z):
	z = np.array(z, dtype=np.float64)
	return 1.0/(1.0+np.exp(z))


class App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.x = self.y = 0

		# Creating elements
		self.canvas = tk.Canvas(self, width=300, height=300, bg = "white", cursor="cross")
		self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
		self.classify_btn = tk.Button(self, text = "Recognise", command = self.classify_handwriting) 
		self.button_clear = tk.Button(self, text = "Clear", command = self.clear_all)
		
		# Grid structure
		self.canvas.grid(row=0, column=0, pady=2, sticky=W,)
		self.label.grid(row=0, column=1,pady=2, padx=2)
		self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
		self.button_clear.grid(row=1, column=0, pady=2)
		# self.canvas.bind("<Motion>", self.start_pos)
		self.canvas.bind("<B1-Motion>", self.draw_lines)


	def clear_all(self):
		self.canvas.delete("all")

	def classify_handwriting(self):
		HWND = self.canvas.winfo_id() # get the handle of the canvas
		rect = win32gui.GetWindowRect(HWND) # get the coordinate of the canvas
		im = ImageGrab.grab(rect)
		digit = predict_digit(im)
		self.label.configure(text= "Digit : " + str(digit)) # +', '+ str(int(acc*100))+'%'
	
	def draw_lines(self, event):
		self.x = event.x
		self.y = event.y
		r=8
		self.canvas.create_oval(self.x-r, self.y-r, self.x + r, self.y + r, fill='black')

app = App()
mainloop()