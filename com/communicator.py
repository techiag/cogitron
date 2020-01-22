import com.fakeserial as emu
import serial as real
import time

class Communicator(object):
    def __init__(self, motorUSB="emu", sensorUSB="emu"):
        '''Sets up either emulator serial or serial connection
        to real devices'''
    
        self.con_nodes = []
        self.deviceHash = {"MotorSerial" : 0, "SensorSerial" : 1}

        '''Create a connection to each slave'''
        self.motor_serial = real.Serial(motorUSB, 9600)# if motorUSB is not "emu" else emu.Serial(9600)
        self.sensor_serial = real.Serial(sensorUSB, 115200)if motorUSB is not "emu" else emu.Serial(9600)

        '''Add connected slaves to list'''
        self.con_nodes.append(self.motor_serial)
        self.con_nodes.append(self.sensor_serial)


    def getConnection(self, string):
        '''Return the right connection based on string'''
        if (string.lower() == "motor"):
            return self.con_nodes[self.deviceHash["MotorSerial"]]
        elif (string.lower() == "sensor"):
            return self.con_nodes[self.deviceHash["SensorSerial"]]


    def sendMessage(self,connection, message):
        messageToBytes = bytes(message, 'utf-8')
        connection.write(messageToBytes)

    def receiveMessage(self, connection):
        #messageReceived = str(connection.readline()[:-2])
        #return messageReceived
        messageReceived = ""
        
        time.sleep(0.5) # in_waiting won't work without this time sleep.
        
        while connection.in_waiting > 0:
            byteReceived = ord(connection.read())
            #print(byteReceived)
            letter = chr(byteReceived)
            if(letter != ""):
                messageReceived += letter
        return messageReceived

        
