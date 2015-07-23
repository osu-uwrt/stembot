import signal
import socket
import RPi.GPIO as GPIO

# SIGINT Handler

def shutdown(signal, frame):

    print '  Stopping UDP.'
    sock.close()

    print '  Stopping PWM.'
    port.stop()
    stbd.stop()
    vert.stop()

    print '  Cleaning up.'
    GPIO.cleanup(PORT)
    GPIO.cleanup(STBD)
    GPIO.cleanup(VERT)

    print '  Exit.'
    exit(0)

signal.signal(signal.SIGINT, shutdown)

# UDP Constants
ADDR = ('localhost', 1337)

# PWM Constants
FREQ = 50
PORT = 18
STBD = 16
VERT = 12

# UDP Setup

print '  Set UDP mode...'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print '  Set UDP bind...'
sock.bind(ADDR)

# PWM Setup

print '  Set GPIO mode...'
GPIO.setmode(GPIO.BOARD)

print '  Set GPIO pins...'
GPIO.setup(PORT, GPIO.OUT)
GPIO.setup(STBD, GPIO.OUT)
GPIO.setup(VERT, GPIO.OUT)

print '  Set PWM frequency...'
port = GPIO.PWM(PORT, FREQ)
stbd = GPIO.PWM(STBD, FREQ)
vert = GPIO.PWM(VERT, FREQ)

print '  Set PWM duty cycle...'
port.start(7.5)
stbd.start(7.5)
vert.start(7.5)

# The Loop

print '  Ready!'
while 1:
    try:
        data = bytearray(2)
        size, addr = sock.recvfrom_into(data)

        if data[0] == 218:
            port.ChangeDutyCycle(data[1])
        elif data[0] == 216:
            stbd.ChangeDutyCycle(data[1])
        elif data[0] == 212:
            vert.ChangeDutyCycle(data[1])
        else:
            print 'Bad packet received.'

    except socket.error as (code, msg):
        pass