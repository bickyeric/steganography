#!/usr/bin/env python3

from Crypto.Cipher import AES

class AESCipher:
  def __init__(self, key):
    self.key = str.encode(key)

  def encrypt(self, msg):
    cipher = AES.new(self.key, AES.MODE_ECB)
    cipherText = cipher.encrypt(str.encode(msg))
    return cipherText.hex()

  def decrypt(self, cipherText):
    decipher = AES.new(self.key, AES.MODE_ECB)
    msg = decipher.decrypt(bytes.fromhex(cipherText))
    return msg

if __name__ == "__main__":
  c = AESCipher("abcdefghijklmnop")

  secret = "SepertiYangBiasa"
  print(secret)

  cipherText = c.encrypt(secret)
  print(cipherText)

  secret = c.decrypt(cipherText)
  print(secret)