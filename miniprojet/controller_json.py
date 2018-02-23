# Program to control passerelle between Android application
# and micro-controller through USB tty
import time
import argparse
import signal
import sys
import serial
import simplejson as json
import datetime 

FILENAME        = "/home/pi/values.json"
VALUES          = '{"values": []}'

# send serial message 
SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 115200
ser = serial.Serial()

def initUART():        
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.port=SERIALPORT
        ser.baudrate=BAUDRATE
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        ser.timeout = None          #block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        #ser.writeTimeout = 0     #timeout for write
        print 'Starting Up Serial Monitor'
        try:
                ser.open()
        except serial.SerialException:
                print("Serial {} port not available".format(SERIALPORT))
                exit()



# Main program logic follows:
if __name__ == '__main__':
        initUART()
        #f= open(FILENAME,"a")
        try:
                with open(FILENAME, 'r') as fin:
                        VALUES = json.load(fin)
        except FileNotFoundError:
                pass

        data=json.loads(VALUES)
        
        print ('Press Ctrl-C to quit.')
        try:
                while ser.isOpen() : 
                        # time.sleep(100)
                        if (ser.inWaiting() > 0): # if incoming bytes are waiting 
                                data_str = ser.readline().strip().strip('\x00').strip() 
                                # print(repr(data_str))
				json_data = json.loads(data_str)
                                json_data["date"] = unicode(datetime.datetime.now())
                                jstr = json.dumps(json_data, indent=4)
                                data["values"].append(json_data)
                                # f.write(jstr)
                                print(jstr)
        except (KeyboardInterrupt, SystemExit):
                if data:
                        with open(FILENAME, 'w') as fout:
                                json.dump(data, fout)
                ser.close()
                exit()
