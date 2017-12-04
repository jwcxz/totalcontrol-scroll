#!/usr/bin/python2

import pygame.midi as pm
import pymouse
import time
import signal, sys

devsig = ('ALSA', 'TotalTrack Control MIDI 1', 1, 0, 0);
tc = None;

def endthis(a,b):
    if tc != None:
        print "Closing device"
        tc.close();
        pm.quit();

    sys.exit(0);
signal.signal(signal.SIGINT, endthis);
signal.signal(signal.SIGTERM, endthis);

# initialize mouse
mouse = pymouse.PyMouse();

# initialize MIDI, find controller
pm.init();
for i in xrange(pm.get_count()):
    _ = pm.get_device_info(i)
    print _;
    if _ == devsig:
        tc = pm.Input(i);
        print " -> Found";
        break;

if tc == None:
    print "Didn't find controller";
    sys.exit(1);

# main loop
while True:
    while not tc.poll():
        sem = 1;
        time.sleep(.02);

    while True:
        pkt = tc.read(1);
        if pkt == []:
            break;
        elif sem > 0 and pkt[0][0][1] in [25, 24]:
            pkt = pkt[0][0];
            offs = 0;
            if pkt[1] == 25:
                # left scroll wheel
                #print "Left wheel", pkt[2];
                offs += 0;
            elif pkt[1] == 24:
                # right scroll wheel
                #print "Right wheel", pkt[2];
                offs += 2;

            if pkt[2] >= 65:
                offs += 0;
            else:
                offs += 1;

            x,y = mouse.position();
            mouse.press(x,y,4+offs);
            mouse.release(x,y,4+offs);

            sem -= 1;
