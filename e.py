from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import os, pathlib

file_path = pathlib.Path(__file__).parent.absolute() # get file's path
k = get_random_bytes(16)
count = 1

pk = RSA.import_key(open("receiver.pem").read())
file_out = open("CK.bin", "wb")
cipher_rsa = PKCS1_OAEP.new(pk)
Ck = cipher_rsa.encrypt(k)
file_out.write(Ck)
file_out.close()
counter = 0

cipher = AES.new(k, AES.MODE_CBC)

#for all the files in the same directory, check for .txt files and encrypt message store into CM_bytes and write out to individual CM_files
for filename in os.listdir(file_path):
	if filename.endswith(".txt"):
		contents = open(filename, "rb")
		M = contents.readline()	
		CM_out = open("CM_file" + str(count) + ".enc" ,"wb")		
		CM_bytes = cipher.encrypt(pad(M, AES.block_size))
		CM_out.write(CM_bytes)
		iv = cipher.iv	# generate number of iv_file per .txt file found
		iv_out = open("iv_file" + str(count), "wb")
		iv_out.write(iv)
		count = count + 1
		cipher = AES.new(k, AES.MODE_CBC)
		print(filename + " successfully encrypted")

if count == 1:
	print("No txt file to encrypt!")
	
