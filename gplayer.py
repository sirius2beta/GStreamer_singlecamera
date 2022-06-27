import paho.mqtt.client as mqtt
import gi
import os
import subprocess
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib, GObject

GROUND1 = 'ground1'
USV1 =  'usv1'

#get video format from existing camera devices
def get_video_format():	
	camera_format = []
	#Check camera device
	for i in range(0,5):
			try:
				cmd = "v4l2-ctl -d /dev/video{} --list-formats-ext".format(i)
				returned_value = subprocess.check_output(cmd,shell=True)  # returns the exit code in unix
			except:
				continue
			line_list = returned_value.split("\n")
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
	return camera_format

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe(USV1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	head = str(msg.payload).split()[0]
	print(head)
	if head == 'qformat':
		video_format = get_video_format()
		client.publish(GROUND1, USV1+'\n'.join(video_format))
		print('publish format')
	


GObject.threads_init()
Gst.init(None)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("114.33.252.156", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()


GObject.threads_init()
Gst.init(None)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("114.33.252.156", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
