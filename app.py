#!/usr/bin/env python3

import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk
from lsb import LSB

class Activity:
  master = tk.Tk()

  image = None
  imgPanel = None

  keyInput = None
  messageInput = None
  path = "./dst.png"

  def __init__(self, path):
    self.image = cv2.imread(path)
    self.updateImage()

    btnFrame = tk.Frame(self.master)
    btnFrame.pack()
    encodeBtn = tk.Button(btnFrame, text = 'Encode', command = self.encode)
    encodeBtn.pack(side = tk.LEFT)
    decodeBtn = tk.Button(btnFrame, text = 'Decode', command = self.decode)
    decodeBtn.pack(side = tk.LEFT)

    saveBtn = tk.Button(self.master, text = 'Save', command = self.save)
    saveBtn.pack()

    tk.Label(self.master, text='Key').pack()
    self.keyInput = tk.Entry(self.master)
    self.keyInput.pack()

    tk.Label(self.master, text='Secret Message').pack()
    self.messageInput = tk.Text(self.master, height=10, width=60)
    self.messageInput.pack()

  def updateImage(self):
    image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    if self.imgPanel == None:
      self.imgPanel = tk.Label(image=image)
      self.imgPanel.image = image
      self.imgPanel.pack(side="top", padx=10, pady=10)
    else:
      self.imgPanel.configure(image = image)
      self.imgPanel.image = image

  def encode(self):
    key = self.keyInput.get()
    message = self.messageInput.get("1.0",'end-1c')

    obj = LSB(self.image)
    obj.embed(message)
    self.messageInput.delete(1.0, tk.END)
    self.image = obj.image

    self.updateImage()

  def decode(self):
    obj = LSB(self.image)
    self.messageInput.delete(1.0, tk.END)
    self.messageInput.insert(tk.INSERT, obj.extract())

  def save(self):
    path = asksaveasfilename(title = "Select file",filetypes=[("png files", "*.png")])
    obj = LSB(self.image)
    obj.save(path)

    messagebox.showinfo("Info", "Saved")

  def startLoop(self):
    self.master.mainloop()

if __name__ == "__main__":
  path = askopenfilename()
  if not isinstance(path, str):
    exit(0)
  app = Activity(path)
  app.startLoop()