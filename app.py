#!/usr/bin/env python3

import cv2
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image, ImageTk
from lsb import LSB
from aes import AESCipher

class Activity:
  master = tk.Tk()

  image = None
  imgPanel = None

  keyInput = None
  messageInput = None
  path = "./dst.png"

  def __init__(self, path):
    self.master.title('AES + Steganography')
    self.image = cv2.imread(path)
    self.updateImage()

    openBtn = tk.Button(self.master, text = 'Open', command = self.openImage)
    openBtn.pack()

    btnFrame = tk.Frame(self.master)
    btnFrame.pack()
    encodeBtn = tk.Button(btnFrame, text = 'Encode', command = self.encode)
    encodeBtn.pack(side = tk.LEFT)
    decodeBtn = tk.Button(btnFrame, text = 'Decode', command = self.decode)
    decodeBtn.pack(side = tk.LEFT)

    saveBtn = tk.Button(self.master, text = 'Save', command = self.saveImage)
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

  def cipher(self):
    key = self.keyInput.get()
    if len(key) != 16:
      messagebox.showwarning("Warning","Key must be 16 character")
      return

    return AESCipher(self.keyInput.get())

  def encode(self):
    message = self.messageInput.get("1.0",'end-1c')
    if len(message)%16 != 0:
      messagebox.showwarning("Warning","Secret Message length must be multiple of 16")
      return

    cipher = self.cipher()
    if cipher == None:
      return
    cipherText = cipher.encrypt(message)

    obj = LSB(self.image)
    obj.embed(cipherText)
    self.messageInput.delete(1.0, tk.END)
    self.image = obj.image

    self.updateImage()
    messagebox.showinfo("Info", "Encoded")

  def decode(self):
    cipher = self.cipher()
    if cipher == None:
      return

    obj = LSB(self.image)

    cipherText = obj.extract()
    msg = cipher.decrypt(cipherText)

    self.messageInput.delete(1.0, tk.END)
    self.messageInput.insert(tk.INSERT, msg)

  def openImage(self):
    path = askopenfilename()
    if not isinstance(path, str):
      return

    self.image = cv2.imread(path)
    self.updateImage()

  def saveImage(self):
    path = asksaveasfilename(title = "Select file",filetypes=[("png files", "*.png")])
    if not isinstance(path, str):
      return

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