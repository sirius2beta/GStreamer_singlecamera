import paho.mqtt.client as mqtt
import gi
import os
import subprocess
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib, GObject


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("COAST")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	import paho.mqtt.client as mqtt
import gi
import os
import subprocess
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib, GObject


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("COAST")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	for i in range(1,5):
		try:
			cmd = "v4l2-ctl -d /dev/video{} --list-formats-ext".format(i)
			returned_value = subprocess.check_output(cmd,shell=True)  # returns the exit code in unix
			line_list = returned_value.split("\n")
			form = ''
			size = ''
			new_line_list = list()
			for i in line_list:
				if len(i.split()) == 0:
					continue
				elif i.split()[0][0] =='[':
					form = i.split()[0][1]
				elif i.split()[0] =='Size:':
					size = i.split()[2]
					print(i)
				elif i.split()[0] == 'Interval:':
					print('{} {} {}'.format(form, size, i.split()[3][1:]))
		except:
			continue
    print(msg.topic+" "+str(msg.payload))


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
