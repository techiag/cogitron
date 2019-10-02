import fakeSerial as emu
import serial as real
import time


class Communicator(object):
    def __init__(self, communicator):
        if communicator == "emu":
            self.com = emu.Serial(9600)
        elif communicator == "real":
            self.com = real.Serial("/dev/tty.usbmodem14101", 9600)

    def sendMessage(self, message):
        messageToBytes = bytes(message, 'utf-8')
        self.com.write(messageToBytes)


    def receiveMessage(self):
        messageReceived = ""
        
        time.sleep(0.5) # in_waiting won't work without this time sleep.
       
        while self.com.in_waiting >0:
            byteReceived = ord(self.com.read())
            letter = chr(byteReceived)
            if(letter != ""):
                messageReceived += letter
        return messageReceived


if __name__ == "__main__":
    '''The emulator is not working, especially because their is not attribute in_waiting, to tell the buffer size
    But! Commmunication seems to be working both ways'''

    bob = Communicator("real") #instance of Communicator
    messageOut = "driveForward" #the message to send to arduino
    
    while True:
        print(bob.receiveMessage()) 
        bob.sendMessage(messageOut)

