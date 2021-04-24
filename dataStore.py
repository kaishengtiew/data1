# Do not run this example program directly. You run this program indirectly
# through the "launcher.py"

import time
from grovepi import *
from grove_rgb_lcd import *
import datetime
from firebase import firebase

firebaseConn = firebase.FirebaseApplication('https://iot-f8e2f-default-rtdb.firebaseio.com/', None)

Sound = 2
dhtsensor = 6


pinMode(Sound,"INPUT")
pinMode(dhtsensor, "INPUT")


'''
D1: Generic digital pin
D3: Yellow Button
A2: Potentiometer
D4: Car reverse sensor (ultrasonic)
A1: Thermistor (temperature sensor)
D6: DHT (humidity and temperature sensor)
'''
BUZZER = 3


state = 0             # Keep D1 state
repeat = 100          # Repeat 100 times

setText('This uses fake modules for rapid development')
while repeat > 0:
    print(f'D1: {digitalRead(1)},  Motion Sensor: {digitalRead(3)},  ' 
          f'Sound: {analogRead(2)}, Food Ultrasonic: {ultrasonicRead(4)},  ')
    #print(f'Thermistor: {temp(1):.2f}\xb0C,  DHT: {t}\xb0C, {h}%')
    state ^= 1
    digitalWrite(1, state)
    time.sleep(0.25)
    
    dataUltra = ultrasonicRead(4)
    #db.child("control").update({'ultra': dataUltra})
    
    repeat -= 1

while True:
    try:     
        [temp,hum] = dht(dhtsensor,0)
        SoilMoisture = analogRead(Sound)
        
        m = str(SoilMoisture)
        t = str(temp)
        h = str(hum)
        
        x = datetime.datetime.now()
        date = x.strftime("%Y%m%d")
        hour = x.strftime("%H")
        minutes = x.strftime("%M")
        HM = x.strftime("%H:%M")

        data_upload = {
            "sound" : m,
            "tempe" : t,
            "humid" : h
        }
        
        result = firebaseConn.patch('Status/' + date + '/' + hour + '/' + minutes, data_upload)
        time.sleep(60)
    except KeyboardInterrupt:
        break
    except IOError:
        print ("Error")


