import gi
import os
import subprocess
import time
import threading
import socket

gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib, GObject

BOAT_NAME = 'usv1'
GROUND_NAME = 'ground1'

PC_IP='10.10.10.205'
SERVER_IP = ''
CLIENT_IP = '127.0.0.1' #PC IP
S_CLIENT_IP = '127.0.0.1'
OUT_PORT = 50008
IN_PORT = 50007 

pipelinesexist = []
pipelines = []
pipelines_state = []
cameraformat = []

def aliveSignal():
	global BOAT_NAME
	global CLIENT_IP
	global S_CLIENT_IP
	print('client started...')
	t = threading.current_thread()
	while getattr(t, "do_run", True):
		beat = 'alive ' + BOAT_NAME
		try:
			client.sendto(beat.encode(),(CLIENT_IP,OUT_PORT))
			time.sleep(0.5)
			print(f"Primary send to: {CLIENT_IP}:{OUT_PORT}")
		except:
			print(f"Primary unreached: {CLIENT_IP}:{OUT_PORT}")
		try:
			client.sendto(beat.encode(),(S_CLIENT_IP,OUT_PORT))
			time.sleep(0.5)
			print(f"Secondarysend to: {S_CLIENT_IP}:{OUT_PORT}")
		except:
			print(f"Secondary unreached: {S_CLIENT_IP}:{OUT_PORT}")

def createPipelines():
	_pipelines = []
	_pipelinesexist = []
	camera_format = get_video_format()
	for i in camera_format:
		j = int(i.split()[0][5]);
		if(j not in _pipelinesexist):
			pipeline = Gst.Pipeline()
			_pipelines.append(pipeline)
			_pipelinesexist.append(j)
	print(_pipelinesexist)
	return _pipelinesexist, _pipelines, camera_format
	

#get video format from existing camera devices
def get_video_format():	
	camera_format = []
	
	#Check camera device
	for i in range(0,10):
			try:
				cmd = "v4l2-ctl -d /dev/video{} --list-formats-ext".format(i)
				returned_value = subprocess.check_output(cmd,shell=True).replace(b'\t',b'').decode("utf-8")  # returns the exit code in unix
			except:
				continue
			line_list = returned_value.splitlines()
			new_line_list = list()
			for j in line_list:
				if len(j.split()) == 0:
					continue
				elif j.split()[0][0] =='[':
					form = j.split()[1][1:-1]
				elif j.split()[0] =='Size:':
					size = j.split()[2]
					width, height = size.split('x')
				elif j.split()[0] == 'Interval:':
					camera_format.append('video{} {} width={} height={} framerate={}'.format(i,form, width, height , j.split()[3][1:].split('.')[0]))
					print('video{} {} width={} height={} framerate={}'.format(i,form, width, height , j.split()[3][1:].split('.')[0]))
	return camera_format

def listenLoop(ser):
	
	global BOAT_NAME
	global CLIENT_IP
	global S_CLIENT_IP
	global OUT_PORT
	print('server started...')
	t = threading.current_thread()
	while getattr(t, "do_run", True):
		try:
			indata, addr = server.recvfrom(1024)
			indata = indata.decode()
		except:
			continue

		#print(f'message from: {str(addr)}, data: {indata}')
		header = indata.split()[0]

		if header == 'HB':
			#thread_cli.Client_ip = indata.split()[1]
			
			BOAT_NAME = indata.split()[2]
			primary = indata.split()[3]
			if primary == 'P':
				CLIENT_IP = indata.split()[1]
			else:
				S_CLIENT_IP = indata.split()[1]

		if header == 'qformat':
			print("format")
			msg = 'format '+BOAT_NAME+'\n'+'\n'.join(cameraformat)

			client.sendto(msg.encode(),(CLIENT_IP,OUT_PORT))
			client.sendto(msg.encode(),(S_CLIENT_IP,OUT_PORT))
		if header == 'cmd':
			print("cmd")
			print(indata)
			cformat = indata.split()[1:6]
			
			print(cformat)
			encoder, mid, quality, ip, port = indata.split()[6:]
			print(quality, ip, port)

			if(' '.join(cformat) not in cameraformat):
				print('format error')
			else:
				gstring = 'v4l2src device=/dev/'+cformat[0]
				if cformat[1] == 'YUYV':
					cformat[1] = 'YUY2'
					gstring += ' num-buffers=-1 ! video/x-raw,format={},width={},height={},framerate={}/1 ! '.format(cformat[1],cformat[2].split('=')[1],cformat[3].split('=')[1],cformat[4].split('=')[1])
					if mid != 'nan':
						gstring += (mid+' ! ')
					if encoder == 'h264':
						gstring +=' videoconvert ! omxh264enc ! rtph264pay pt=96 config-interval=1 ! udpsink host={} port={}'.format(ip, port)
						
					else:
						gstring +='jpegenc quality={} ! rtpjpegpay ! udpsink host={} port={}'.format(quality,ip, port)
				elif cformat[1] == 'MJPG':
                                        gstring += ' num-buffers=-1 ! image/jpeg,width={},height={},framerate={}/1 ! '.format(cformat[2].split('=')[1],cformat[3].split('=')[1],cformat[4].split('=')[1])
                                        if mid != 'nan':
                                                gstring += (mid+' ! ')
                                        gstring +='jpegparse ! rtpjpegpay ! udpsink host={} port={}'.format(ip, port)
				elif cformat[1] == 'GREY':
					gstring += ' num-buffers=-1 ! video/x-raw,format=GRAY8 ! videoscale ! videoconvert ! video/x-raw, format=YUY2, width=640,height=480 ! videoconvert !  '
					if mid != 'nan':
						gstring += (mid+' ! ')
					gstring +='jpegenc ! rtpjpegpay ! udpsink host={} port={}'.format(ip, port)
				else:
					if cformat[1] == 'RGBP':
						cformat[1] = 'RGB16'
					elif cformat[1] == 'BGR8':
						cformat[1] = 'BGR'
					elif cformat[1] == 'Y1':
						cformat[1] = 'UYVY'
					gstring += ' num-buffers=-1 ! video/x-raw,format={}! videoscale ! videoconvert ! video/x-raw, format=YUY2, width=640,height=480 ! videoconvert ! '.format(cformat[1])
					if mid != 'nan':
						gstring += (mid+' ! ')
					gstring +='jpegenc ! rtpjpegpay ! udpsink host={} port={}'.format(ip, port)

				
				print(gstring)
				print(cformat[1])
				print(cformat[1][5:])
				videoindex = pipelinesexist.index(int(cformat[0][5:]))
				

				if pipelines_state[videoindex] == True:
					pipelines[videoindex].set_state(Gst.State.NULL)
					pipelines[videoindex] = Gst.parse_launch(gstring)
					pipelines[videoindex].set_state(Gst.State.PLAYING)

				else:
					pipelines[videoindex] = Gst.parse_launch(gstring)
					pipelines[videoindex].set_state(Gst.State.PLAYING)
					pipelines_state[videoindex] = True
		if header == 'quit':
			video = int(indata.split()[1][5:])
			if video in pipelinesexist:
				videoindex = pipelinesexist.index(video)
				pipelines[videoindex].set_state(Gst.State.NULL)
				pipelines_state[videoindex] = False
				print("quit : video"+str(video))



# The callback for when the client receives a CONNECT response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(BOAT_NAME)
	aliveThread = threading.Thread(target = aliveSignal)
	aliveThread.start()

# The callback for when a PUBLISH message is received from the server.



GObject.threads_init()
Gst.init(None)

pipelinesexist, pipelines, cameraformat = createPipelines()
for i in pipelines:
	pipelines_state.append(False)

#client = mqtt.Client()
#client.on_connect = on_connect
#client.on_message = on_message
#while True:
#	try:
#		client.connect("test.mosquitto.org", 1883, 60)
#	except:
#		time.sleep(10)
#		continue
#	break

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.

#client.loop_forever()

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_IP, IN_PORT))
server.setblocking(0)

print(f'server started at {IN_PORT}')
print(f'send message to {CLIENT_IP}, Port: {IN_PORT}')

lock = threading.Lock()

thread_cli = threading.Thread(target=aliveSignal)
thread_ser = threading.Thread(target=listenLoop, args=(server,))

thread_cli.Client_ip = "192.168.0.1"

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
