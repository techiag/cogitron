#import com.fakeserial as emu
import serial as real
import time

class Communicator(object):
    def __init__(self, communicator):
        '''Sets up either emulator serial or serial connection
        to real devices'''

        if communicator == "emu":
            pass
            #self.com = emu.Serial(9600)
        elif communicator == "real":
            self.con_nodes = []
            self.deviceHash = {"Motor" : 0, "Sensor" : 1}

            '''Create a connection to each slave'''
            self.motor = real.Serial("/dev/cu.usbmodem14101", 9600)
            self.sensor = real.Serial("/dev/tty.usbmodem14201", 9600)

            '''Add connected slaves to list'''
            self.con_nodes.append(self.motor)
            self.con_nodes.append(self.sensor)

    def getConnection(self, string):
        '''Return the right connection based on string'''
        if (string.lower() == "motor"):
            return self.con_nodes[self.deviceHash["Motor"]]
        elif (string.lower() == "sensor"):
            return self.con_nodes[self.deviceHash["Sensor"]]


    def sendMessage(self,connection, message):
        messageToBytes = bytes(message, 'utf-8')
        connection.write(messageToBytes)

    def receiveMessage(self, connection):
        messageReceived = ""

        time.sleep(0.5)  # in_waiting won't work without this time sleep.

        while connection.in_waiting > 0:
            byteReceived = ord(connection.read())
            #print(byteReceived)
            letter = chr(byteReceived)
            if(letter != ""):
                messageReceived += letter
        return messageReceived

if __name__ == "__main__":
    '''The emulator is not working, especially because there is not attribute in_waiting in emulator, to tell the buffer size
    Real serial connection works'''

    bob = Communicator("real")  # instance of Communicator
    messageOut = "setMotors;1;2;2"  # the message to send to arduino

    while True:
        print(bob.receiveMessage(bob.getConnection("motor")))
        messageOut = input("\nenter command\n")
        bob.sendMessage(messageOut)