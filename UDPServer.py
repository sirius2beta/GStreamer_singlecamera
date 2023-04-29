import socket
import threading
import time

BOAT_NAME = 'usv1'
GROUND_NAME = 'ground1'

SERVER_IP = ''
CLIENT_IP = '100.117.209.85' #Boat IP
OUT_PORT = 50008  
IN_PORT = 50007  

exit_loop = False


def aliveSignal(cli, to_addr):
	print('client started...')
	t = threading.current_thread()
	while getattr(t, "do_run", True):
		beat = 'alive ' + BOAT_NAME
		cli.sendto(beat.encode(),to_addr)
		time.sleep(1)
		
def listenLoop(ser):
	print('server started...')
	t = threading.current_thread()
	while getattr(t, "do_run", True):
		try:
			indata, addr = server.recvfrom(1024)
			indata = indata.decode()
			print(f'message from: {str(addr)}, data: {indata}')
			# handle indata
		except:
			continue


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_IP, IN_PORT))
server.setblocking(0)

print(f'server started at {IN_PORT}')
print(f'send message to {CLIENT_IP}, Port: {IN_PORT}')

thread_cli = threading.Thread(target=aliveSignal, args=(client, (CLIENT_IP, OUT_PORT)))
thread_ser = threading.Thread(target=listenLoop, args=(server,))
thread_cli.start()
thread_ser.start()

try:
	input("Press the Enter key to exit: ")
except:
	thread_ser.do_run = False
	thread_cli.do_run = False
	thread_cli.join()
	thread_ser.join()
thread_ser.do_run = False
thread_cli.do_run = False
thread_cli.join()
thread_ser.join()
