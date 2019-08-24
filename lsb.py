#!/usr/bin/env python3

import cv2

class AppError(BaseException):
  pass

def i2bin(i, l):
  actual = bin(i)[2:]
  if len(actual) > l:
    raise AppError("bit size is larger than expected.")

  while len(actual) < l:
    actual = "0"+actual

  return actual

def char2bin(c):
  return i2bin(ord(c), 8)

class LSB():

  MAX_BIT_LENGTH = 16

  def __init__(self, img):
    self.size_x, self.size_y, self.size_channel = img.shape

    self.image = img
    self.cur_x = 0
    self.cur_y = 0
    self.cur_channel = 0

  def next(self):
    if self.cur_channel != self.size_channel-1:
      self.cur_channel += 1
    else:
      self.cur_channel = 0
      if self.cur_y != self.size_y-1:
        self.cur_y += 1
      else:
        self.cur_y = 0
        if self.cur_x != self.size_x-1:
          self.cur_x += 1
        else:
          raise AppError("need larger image")

  def put_bit(self, bit):
    v = self.image[self.cur_x, self.cur_y][self.cur_channel]

    binaryV = bin(v)[2:]

    # replace last bit if different
    if binaryV[-1] != bit:
      binaryV = binaryV[:-1]+bit

    self.image[self.cur_x, self.cur_y][self.cur_channel] = int(binaryV,2)
    self.next()

  def put_bits(self, bits):
    for bit in bits:
      self.put_bit(bit)

  def read_bit(self):
    v = self.image[self.cur_x, self.cur_y][self.cur_channel]
    return bin(v)[-1]

  def read_bits(self, length):
    bits = ""
    for _ in range(0, length):
      bits += self.read_bit()
      self.next()

    return bits

  def embed(self, text):
    text_length = i2bin(len(text), self.MAX_BIT_LENGTH)
    self.put_bits(text_length)

    for c in text:
      bits = char2bin(c)
      self.put_bits(bits)

  def extract(self):
    length = int(self.read_bits(self.MAX_BIT_LENGTH), 2)
    text = ""
    for _ in range(0, length):
      c = int(self.read_bits(8), 2)
      text += chr(c)

    return text

  def save(self, dstPath):
    cv2.imwrite(dstPath, self.image)

if __name__ == "__main__":
  # obj = LSB(cv2.imread('src.jpg'))
  # obj.embed("ku yakin pasti suatu saat semua kan terjadi, kau kan mencintaiku dan tak akan pernah melepasku aku mau mendampingi dirimu, aku mau cintai kekuranganmu, s'lalu bersedia bahagiakanmu apapun terjadi, kujanjikan aku ada...")

  obj = LSB(cv2.imread('dst.png'))
  text = obj.extract()
  print(text)
