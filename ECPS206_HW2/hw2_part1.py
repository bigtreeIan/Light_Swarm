import time
import Adafruit_TCS34725
import smbus
import RPi.GPIO as GPIO
import threading

blueLed = 11
greenLed = 13
redLed = 15
whiteLed = 29
pushButton = 31
motionSensor = 33
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pushButton, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(motionSensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(redLed, GPIO.OUT)
GPIO.setup(greenLed, GPIO.OUT)
GPIO.setup(blueLed, GPIO.OUT)
GPIO.setup(whiteLed, GPIO.OUT)
slidingWindow1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
slidingWindow2 = [0, 0, 0, 0, 0, 0]
idx = 0
avglux = 0.0000001
flashTime = 0.000001
#press for part2
press = False
#flag for part3
flag = False
bright = 0
timeLimit = 10

############################part2############################################
#def ISR(channel):
#    global press
#    press = not press
#GPIO.add_event_detect(pushButton, GPIO.RISING, callback=ISR, bouncetime=200)
############################end part2########################################

############################part3############################################
#def stopReading():
#    global flag
#    flag = False
#timeThread = threading.Timer(timeLimit, stopReading)
#
#def ledFlash():
#    print("in")
#    global flashTime
#    global flag
#    while True:
#        time.sleep(0.001)
#        while flag:
#            print(flashTime)
#            time.sleep(flashTime)
#            GPIO.output(whiteLed, True)
#            time.sleep(flashTime)
#            GPIO.output(whiteLed, False)
#t = threading.Thread(target = ledFlash)
#t.start()
#
#def ISR2(channel):
#    global timeThread
#    global flag
#    flag = True
#    if timeThread.is_alive():
#        timeThread.cancel()
#    timeThread = threading.Timer(timeLimit, stopReading)
#    timeThread.start()
#
#GPIO.add_event_detect(motionSensor, GPIO.RISING, callback=ISR2)
#
#
############################end part3###########################################
tcs = Adafruit_TCS34725.TCS34725()

while True:
#    GPIO.output(redLed, False)
#    GPIO.output(greenLed, False)
#    GPIO.output(blueLed, False)
#    GPIO.output(whiteLed, False)

#########################part1##########################################
   R, G, B, C = tcs.get_raw_data()
   color_temp = Adafruit_TCS34725.calculate_color_temperature(R, G, B)
   lux = Adafruit_TCS34725.calculate_lux(R, G, B) 
   slidingWindow1[idx % 12] = C
   bright = 0
   for x in range(0, 12):
       bright = bright + slidingWindow1[x]
   avgC = bright / 12
   if R >= 50:
       GPIO.output(redLed, True)
   if G >= 50:
       GPIO.output(greenLed, True)
   if B >= 50:
       GPIO.output(blueLed, True)
   if avgC >= 100:
       GPIO.output(whiteLed, True)
   if R < 50:
       GPIO.output(redLed, False)
   if G < 50:
       GPIO.output(greenLed, False)
   if B < 50:
       GPIO.output(blueLed, False)
   if avgC < 100:
       GPIO.output(whiteLed, False)
   print('Color: red={0} green={1} blue={2} clear={3}'.format(R, G, B, C))
   print('Average C:', avgC)
   idx = idx + 1
   time.sleep(0.25)
#############################end part1########################################
    
##############################part2############################################
#    time.sleep(0.001)
#    while press:
#        R, G, B, C = tcs.get_raw_data()
#        color_temp = Adafruit_TCS34725.calculate_color_temperature(R, G, B)
#        slidingWindow2[idx % 6] = C
#        bright = 0
#        for x in range(0, 6):
#            bright = bright + slidingWindow2[x]
#        avgC = bright / 6
#        if R >= 50:
#            GPIO.output(redLed, True)
#        if G >= 50:
#            GPIO.output(greenLed, True)
#        if B >= 50:
#            GPIO.output(blueLed, True)
#        if avgC >= 100:
#            GPIO.output(whiteLed, True)
#        if R < 50:
#            GPIO.output(redLed, False)
#        if G < 50:
#            GPIO.output(greenLed, False)
#        if B < 50:
#            GPIO.output(blueLed, False)
#        if avgC < 100:
#            GPIO.output(whiteLed, False)
#        print('Color: red={0} green={1} blue={2} clear={3}'.format(R, G, B, C))
#        print('Average C:', avgC)
#        idx = idx + 1
#        time.sleep(0.5)
###############################end part2####################################

##############################part3#########################################
#    time.sleep(0.001)
#    while flag:
#        R, G, B, C = tcs.get_raw_data()
#        color_temp = Adafruit_TCS34725.calculate_color_temperature(R, G, B)
#        lux = Adafruit_TCS34725.calculate_lux(R, G, B) 
#        slidingWindow2[idx % 6] = lux
#        bright = 0
#        for x in range(0, 6):
#            bright = bright + slidingWindow2[x]
#        avglux = bright / 6
#        print("avglux:", avglux)
#        if R >= 50:
#            GPIO.output(redLed, True)
#        if G >= 50:
#            GPIO.output(greenLed, True)
#        if B >= 50:
#            GPIO.output(blueLed, True)
#        if R < 50:
#            GPIO.output(redLed, False)
#        if G < 50:
#            GPIO.output(greenLed, False)
#        if B < 50:
#            GPIO.output(blueLed, False)
#        flashTime = 10.0 / avglux 
#        print('Color: red={0} green={1} blue={2} clear={3}'.format(R, G, B, C))
#        print('Average LUX:', avglux)
#        idx = idx + 1
#        time.sleep(0.5)

###############################end part3####################################
