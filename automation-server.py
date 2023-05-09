#!/usr/bin/env python3
#!/usr/bin/python -tt
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import os
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



set_on=""
set_off=""
switch_state=""
switch_state3=""
current_time=""
flag_entrance_on=""
flag_garage_on=""
flag_firebase_entrance=""
flag_firebase_garage=""
# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(body):

	url = 'https://app.nativenotify.com/api/notification'
	myobj = {"appId": "","appToken": "","title": "","body": body,"dateSent": "1-26-2023 12:04PM",}

	x = requests.post(url, json = myobj)

def firebase_connect():
        cred = credentials.Certificate("")
        firebase_admin.initialize_app(cred)

            
def firebase(text):
	now = datetime.now()
	date_time = now.strftime("%Y-%m-%d  %H:%M:%S")	
	firestore_client = firestore.client() # connecting to firestore
	doc_ref = firestore_client.collection("History").document(date_time)
	doc_ref.set(
    		{
			"user":"Auto",
			"time":date_time,
        		"function": text,
        		
    		}
	)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("switch_state")
    client.subscribe("switch_state3")
    client.subscribe("set_on")
    client.subscribe("set_off")
    client.subscribe("light_status")
    client.subscribe("light_status3")


def on_message(client, userdata, msg):
    
    global switch_state
    global switch_state3
    global current_time
    global set_on
    global set_off
    global flag_garage_on
    global flag_entrance_on
    global flag_firebase_entrance
    global flag_firebase_garage

    current_time=time.strftime("%H%M")
    print ("clock : ",current_time)
    if (msg.topic == 'switch_state'):
      switch_state=msg.payload.decode("utf-8")
      print ("1 : ",switch_state)
    if (msg.topic == 'switch_state3'):
      switch_state3=msg.payload.decode("utf-8")
      print ("3 : ",switch_state3)
    if (msg.topic == 'light_status'):
      light_status=msg.payload.decode("utf-8")
      print ("light : ",light_status)
      print (flag_entrance_on)
      if (flag_entrance_on==""):
         flag_entrance_on=light_status
      if (light_status!=flag_entrance_on):
           if(light_status=="1"):
             send_push_message("Entrance Light On")
           if(light_status=="0"):
             send_push_message("Entrance Light Off")
           flag_entrance_on=light_status
    if (msg.topic == 'light_status3'):
      light_status3=msg.payload.decode("utf-8")
      print ("light3 : ",light_status3)
      print (flag_garage_on)
      if (flag_garage_on==""):
         flag_garage_on=light_status3
      if (light_status3!=flag_garage_on):
           if(light_status3=="1"):
             send_push_message("Garage Light On")
           if(light_status3=="0"):
             send_push_message("Garage Light Off")
           flag_garage_on=light_status3
    if (msg.topic == 'set_on'):
      set_on=msg.payload.decode("utf-8")
      print (set_on)
      file = open("set_on.txt", "w")
      file.write(set_on)
      file.close()
      #os.environ["set_on"]=set_on
    if (msg.topic == 'set_off'):
      set_off=msg.payload.decode("utf-8")
      print (set_off)
      file = open("set_off.txt", "w")
      file.write(set_off)
      file.close()
    if(current_time==set_on):
         print ("on")
         if(switch_state=="1"):
           client.publish("light_switch","1")
          # firebase("Entrance Light On")
           if(flag_firebase_entrance=="0" or flag_firebase_entrance==""):
             print("sent firebase entrance on")
             firebase("Entrance Light On")
             flag_firebase_entrance="1"
             time.sleep(10)
           print ("sent")
         if(switch_state3=="1"):
           client.publish("light_switch3","1")
          # firebase("Garage Light On")
           if(flag_firebase_garage=="0" or flag_firebase_garage==""):
             print("sent firebase garage on")
             firebase("Garage Light On")
             flag_firebase_garage="1"
           print ("sent")
           time.sleep(10)
         if(switch_state=="0"):
           client.publish("light_switch","2")
          # firebase("Entrance Light On")
           if(flag_firebase_entrance=="0" or flag_firebase_entrance==""):
             print("sent firebase entrance on")
             firebase("Entrance Light On")
             flag_firebase_entrance="1"
           print ("sent")
           time.sleep(10)
         if(switch_state3=="0"):
           client.publish("light_switch3","2")
          # firebase("Garage Light On")
           if(flag_firebase_garage=="0" or flag_firebase_garage==""):
             print("sent firebase garage on")
             firebase("Garage Light On")
             flag_firebase_garage="1"
           print ("sent")
           time.sleep(10)
    
    if(current_time==set_off):
         print ("off")
         if(switch_state=="1"):
           client.publish("light_switch","2")
           # firebase("Entrance Light Off")
           if(flag_firebase_entrance=="1" or flag_firebase_entrance==""):
             print("sent firebase entrance off")
             firebase("Entrance Light Off")
             flag_firebase_entrance="0"
           print ("sent")
           time.sleep(10)
         if(switch_state3=="1"):
           client.publish("light_switch3","2")
           # firebase("Garage Light Off")
           if(flag_firebase_garage=="1" or flag_firebase_garage==""):
             print("sent firebase garage off")
             firebase("Garage Light Off")
             flag_firebase_garage="0"
           print ("sent")
           time.sleep(10)
         if(switch_state=="0"):
           client.publish("light_switch","1")
           # firebase("Entrance Light Off")
           if(flag_firebase_entrance=="1" or flag_firebase_entrance==""):
             print("sent firebase entrance off")
             firebase("Entrance Light Off")
             flag_firebase_entrance="0"
           print ("sent")
           time.sleep(10)
         if(switch_state3=="0"):
           client.publish("light_switch3","1")
           # firebase("Garage Light Off")
           if(flag_firebase_garage=="1" or flag_firebase_garage==""):
             print("sent firebase garage off")
             firebase("Garage Light Off")
             flag_firebase_garage="0"
           print ("sent")
           time.sleep(10)
    #if(set_on!="" and set_off!=""): 
    client.publish("time1",set_on)
    time.sleep(1.5)
    client.publish("time2",set_off)
    #print (set_on)
    #print (set_off)

#set_on=os.environ.get("set_on")
firebase_connect();
#write filestamp file if first time
if os.path.exists('set_on.txt') == False:
    file = open("set_on.txt", "w")
    file.write("0000")
    file.close()
if os.path.exists('set_off.txt') == False:
    file = open("set_off.txt", "w")
    file.write("0000")
    file.close()
#read last filestamp file stored
file = open("set_on.txt", "r")
#print(file.read())
set_on=(file.read())
file.close()

file = open("set_off.txt", "r")
#print(file.read())
set_off=(file.read())
file.close()

#print ("start")

#print (set_on)
#print (set_off)

client = mqtt.Client()
client.connect("",,60)
client.on_connect = on_connect
client.on_message = on_message
#time.sleep(1)
client.loop_forever()
