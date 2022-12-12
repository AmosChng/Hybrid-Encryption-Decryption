from base64 import b64decode
from Crypto.Util.Padding import unpad

from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

import os, pathlib

file_path = pathlib.Path(__file__).parent.absolute() # get file's path
file_in = open("CK.bin", "rb")
sk = RSA.import_key(open("private.pem").read())
Ck = file_in.read(sk.size_in_bytes())
cipher_rsa = PKCS1_OAEP.new(sk)
k = cipher_rsa.decrypt(Ck)
file_in.close()
filelist = []

# to display file's name with message
for filename in os.listdir(file_path):
	if filename.endswith('.txt'):
		filelist.append(filename)

try:
	
	for i in range(0, len(filelist)):
		iv_file = open("iv_file" + str(i+1),"rb") 
		iv = iv_file.read()

		CM_file = open("CM_file" + str(i+1) + ".enc" ,"rb")
		CM = CM_file.readline()
		cipher = AES.new(k, AES.MODE_CBC, iv)
		M = unpad(cipher.decrypt(CM), AES.block_size)
		print("The message in " + filelist[i] + " is " + str(M))
		
except ValueError:
	print("Incorrect decryption")
except KeyError:
	print("Incorrect Key")

	
		
