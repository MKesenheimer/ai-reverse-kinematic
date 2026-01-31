import serial

class GCodeSender:
    def __init__(self, port):
        # Open serial port
        self.s = serial.Serial(port, 115200, timeout=1)

    def sendGcode(self, Gcode): # sendet einzelne Gcode befele
        line = Gcode.strip() # Strip all EOL characters for consistency
        print('Sending: ' + line),
        self.s.write((line + '\n').encode()) # Send g-code block to grbl

        Status = None
        grbl_out = b''
        while grbl_out != b'ok\r\n':
            grbl_out = self.s.readline() # Wait for grbl response with carriage return
            if grbl_out != b'\r\n' and grbl_out != b'ok\r\n':
                #print(f'RoboterArm: {grbl_out.strip()}')
                Status = grbl_out
        return Status

if __name__ == "__main__":
    sender = GCodeSender(port = "COM3")
    while True:
        rueckgabewert = sender.sendGcode(input(">>"))

    sender2 = GCodeSender(port = "COM4")
    sender2.sendGcode("G0 A180 F100")