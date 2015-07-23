controller = open('/dev/input/js0','r')

button = [0] * 32
axis = [0] * 32

packet = []

while 1:
    # I just don't know how Python works, do I?
    packet += [int(str(hex(ord(controller.read(1)))), 16)]
    # A complete message:
    if len(packet) == 8:
        # Buttons:
        if packet[6] == 1:
            button[packet[7]] = packet[4]
            print '%i %i %i' % (packet[6], packet[7], packet[4])
        # Axes:
        elif packet[6] == 2:
            if packet[7] < 4:
                axis[packet[7]] = packet[5]
                print '%i %i %i' % (packet[6], packet[7], packet[5])
        # Startup:
        else: 
            print '.'
        # Reset:
        packet = []