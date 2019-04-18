import time
import Adafruit_TCS34725
import smbus
import RPi.GPIO as GPIO
import threading
import socket
import netifaces


addrs = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0].get('addr')
greenLedPi = 13
redLedPi = 15
whiteLedPi = 11
slidingWindowPi = [0,0,0,0,0]
ip_port=(addrs, 4210)
BUFSIZE=1024
idx = 0
avglux = 0
addr = ()
sendmsg = False
disconnectFlag = False
blink = True

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(greenLedPi, GPIO.OUT)
GPIO.setup(redLedPi, GPIO.OUT)
GPIO.setup(whiteLedPi, GPIO.OUT)

tcs = Adafruit_TCS34725.TCS34725()
udp_server_client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udp_server_client.bind(ip_port)
udp_server_client.settimeout(4)


def readESPvalue():
    global addr
    global disconnectFlag
    while True:
        try:
            msg, addr = udp_server_client.recvfrom(BUFSIZE)
            disconnectFlag = False
            print("received", int(msg))
            if(avglux < int(msg)):
                GPIO.output(redLedPi, True)
                GPIO.output(greenLedPi, False)
            else:
                GPIO.output(greenLedPi, True)
                GPIO.output(redLedPi, False)
        except:
            disconnectFlag = True



t = threading.Thread(target = readESPvalue)
t.start()



while True:
        R, G, B, C = tcs.get_raw_data()
        lux = Adafruit_TCS34725.calculate_lux(R, G, B)
        slidingWindowPi[idx % 5] = lux
        totallux = 0
        for i in range(0, 5):
            totallux = totallux + slidingWindowPi[i]
        avglux = totallux / 5
        idx = idx + 1
        print("Pi", avglux)     
        if(addr != () and sendmsg == True):
            udp_server_client.sendto(str(avglux).encode('utf-8'), addr)
        sendmsg = not sendmsg
        if(disconnectFlag == True):
            GPIO.output(whiteLedPi, blink)
        if(disconnectFlag == False):
            GPIO.output(whiteLedPi, False)
        blink = not blink
        time.sleep(1)

#
#
#
#
#
#
#
#
#

