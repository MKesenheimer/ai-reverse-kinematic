import serial
import time

# Open serial port

s = serial.Serial("COM3",115200, timeout=1)

def sendGcode(Gcode): # sendet einzelne Gcode befele
    l = Gcode.strip() # Strip all EOL characters for consistency
    global s
    print('Sending: ' + l),
    s.write((l + '\n').encode()) # Send g-code block to grblÂ³

    Status = None
    grbl_out = b''
    while grbl_out != b'ok\r\n':
        grbl_out = s.readline() # Wait for grbl response with carriage return
        if grbl_out != b'\r\n' and grbl_out != b'ok\r\n':
            #print(f'RoboterArm: {grbl_out.strip()}')
            Status = grbl_out
    return Status

if __name__ == "__main__":
    while True:
        sendGcode(input(">>"))