# Program to control passerelle between Android application
# and micro-controller through USB tty
import time
import argparse
import signal
import sys
import socket
import serial
import threading

HOST           = "0.0.0.0"
UDP_PORT       = 10000
MICRO_COMMANDS = ["TLH" , "THL" , "LTH" , "LHT" , "HTL" , "HLT"]
FILENAME        = "/home/pi/values.txt"
LAST_VALUE      = ""

class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        current_thread = threading.current_thread()
        print("{}: client: {}, wrote: {}".format(current_thread.name, self.client_address, data))
        if data != "":
                        if data in MICRO_COMMANDS: # Send message through UART
                                sendUARTMessage(response)
                                
                        elif data == "getValues()": # Sent last value received from micro-controller
                                socket.sendto(LAST_VALUE, self.client_address) 
                                # TODO: Create last_values_received as global variable      
                        else:
                                print("Unknown message: ",response)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


# send serial message 
SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 115200
ser = serial.Serial(SERIALPORT, BAUDRATE)

def initUART():        
        # ser = serial.Serial(SERIALPORT, BAUDRATE)
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        ser.timeout = None          #block read

        # ser.timeout = 0             #non-block read
        # ser.timeout = 2              #timeout block read
        # ser.xonxoff = False     #disable software flow control
        # ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        # ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        #ser.writeTimeout = 0     #timeout for write
        print 'Starting Up Serial Monitor'
        try:
                ser.open()


def sendUARTMessage(msg):
    ser.write(msg)


# Main program logic follows:
if __name__ == '__main__':
        initUART()
        f= open(FILENAME,"a")
        print ('Press Ctrl-C to quit.')

        server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)

        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True

        try:
                server_thread.start()
                print("Server started at {} port {}".format(HOST, PORT))
                while ser.isOpen() : 
                        # time.sleep(100)
                        if (ser.inWaiting() > 0): # if incoming bytes are waiting 
                                data_str = ser.read(ser.inWaiting()).decode('ascii') #read the bytes and convert from binary array to ASCII
                                f.write(data_str)
                                LAST_VALUE = data_str
                                print(data_str)
        except (KeyboardInterrupt, SystemExit):
                server.shutdown()
                server.server_close()
                f.close()
                exit()