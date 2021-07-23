from m5stack import *
from m5stack_ui import *
from uiflow import *
import wifiCfg
import urequests
import time
import json

import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xaa3838)
finger_10 = unit.get(unit.FINGER, unit.PORTC)
rfid_7 = unit.get(unit.RFID, unit.PORTA)


status = None
DataMap = None
rfidValue = None
accValue = None
RFID = None
json_data = None
accessStatus = None
DoorStatus = None

wifiCfg.autoConnect(lcdShow=True)
touch_button0 = M5Btn(text='Button', x=226, y=44, w=55, h=35, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
image0 = M5Img("res/access.png", x=221, y=29, parent=None)
image1 = M5Img("res/waylay.png", x=110, y=205, parent=None)
image2 = M5Img("res/fingerprint.png", x=34, y=29, parent=None)
deb = M5Label('Text', x=207, y=132, color=0x000, font=FONT_MONT_14, parent=None)
HttpStatus = M5Label('Text', x=34, y=215, color=0x000, font=FONT_MONT_14, parent=None)
ps = M5Label('Text', x=238, y=215, color=0x000, font=FONT_MONT_14, parent=None)
accStat = M5Label('Text', x=11, y=113, color=0x000, font=FONT_MONT_14, parent=None)
read = M5Label('Text', x=11, y=138, color=0x000, font=FONT_MONT_14, parent=None)
RF1 = M5Label('Text', x=238, y=113, color=0x000, font=FONT_MONT_14, parent=None)


# Describe this function...
def CreatePayloadRFID():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  if accessStatus == 1:
    rfidValue = 'Door Unlocked'
    DoorStatus = 1
  else:
    rfidValue = 'Entry Denied'
    DoorStatus = 0
  DataMap = {'RFID':rfidValue,'DoorStatus':DoorStatus}
  json_data = json.dumps(DataMap)

# Describe this function...
def SendPOST():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  status = 'No Status'
  try:
    req = urequests.request(method='POST', url='Fill-in-your-webscript-url',data=json_data, headers={'Content-Type':'application/json'})
    ps.set_text_color(0x006600)
    wait(5)
    status = req.status_code
    ps.set_text('Data sent')
  except:
    ps.set_text_color(0x990000)
    wait(5)
    ps.set_text('Not sent')
  wait(5)
  HttpStatus.set_text(str(status))

# Describe this function...
def CreatePayloadFingerprint():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  if accessStatus == 1:
    accValue = 'Door Unlocked'
    DoorStatus = 1
  else:
    accValue = 'Entry Denied'
    DoorStatus = 0
  DataMap = {'Access':accValue,'DoorStatus':DoorStatus}
  json_data = json.dumps(DataMap)


def touch_button0_pressed():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  RF1.set_text(str(rfid_7.isCardOn()))
  deb.set_text(str(rfid_7.readUid()))
  RFID = rfid_7.readUid()
  wait(0.5)
  if (rfid_7.readUid()) == 'dcbf3abfe6':
    accessStatus = 0
  else:
    accessStatus = 1
  CreatePayloadRFID()
  SendPOST()
  pass
touch_button0.pressed(touch_button0_pressed)

def finger_10_cb(user_id, access):
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  if (access) == 1:
    accStat.set_text('Access Granted')
    accValue = 'Acces Granted'
    SendPOST()
    wait(5)
  else:
    accStat.set_text('Access Denied')
    accValue = 'Acces Denied'
    SendPOST()
    wait(5)
  pass
finger_10.readFingerCb(callback=finger_10_cb)

def buttonA_wasPressed():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  CreatePayloadFingerprint()
  SendPOST()
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  finger_10.addUser(2, 2)
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  finger_10.removeAllUser()
  pass
btnC.wasPressed(buttonC_wasPressed)

def buttonB_pressFor():
  global status, DataMap, rfidValue, accValue, RFID, json_data, accessStatus, DoorStatus
  finger_10.addUser(1, 1)
  pass
btnB.pressFor(0.8, buttonB_pressFor)


import custom.urequests as urequests
while True:
  read.set_text(str(finger_10.state))
  wait_ms(2)

