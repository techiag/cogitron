from communicator import Communicator
if __name__ == "__main__":
    '''The emulator is not working, especially because there is not attribute in_waiting in emulator, to tell the buffer size
    Real serial connection works'''

    motorUSB = "/dev/cu.usbmodem14101"
    sensorUSB = "/dev/tty.usbmodem14201"

    bob = Communicator(motorUSB, sensorUSB)  # instance of Communicator
    messageOut = "setMotor;1;2"  # the message to send to arduino

    while True:
        messageOut = input("\nenter command\n")
        bob.sendMessage(bob.getConnection("motor"), messageOut)
        print(bob.receiveMessage(bob.getConnection("motor")))
