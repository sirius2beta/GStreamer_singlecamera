import socket

HOST = ''
PORT = 50007

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f'server started at {$PORT}')
print(f'waiting for connection')

while True:
	indata, addr = server.recvfrom(1024)
	print('message from: {str(addr), data: {indata.decode()}}
