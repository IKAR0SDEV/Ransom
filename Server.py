import socket

IP_ADDRESS = 'localhost'
PORT = 4567
print('Creating new Socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP_ADDRESS, PORT))
    print('Waiting for Connection')
    s.listen(1)
    conn, addr = s.accept()
    print(f'Connected to {addr} ')
    with conn:
        while True:
            hostDetails = conn.recv(1024).decode()
            with open('Encryption_keys.txt', 'a') as f:
                f.write(hostDetails + '\n')
                break
        print('Connection Closed')
