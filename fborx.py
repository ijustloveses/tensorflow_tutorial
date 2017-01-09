#!/usr/bin/env python
# encoding: utf-8

import pygame
import os
size = (0, 0)

#x and y will be the windowsize if an xserver is running
def getScreen(x,y):
    pygame.init()
    if 'DISPLAY' in os.environ:
        try:
            return getWindow(x,y)
        except:
            return getFb()
    else:
        try:
            return getFb()
        except:
            return getWindow(x,y)

def getWindow(x,y):
    print("Try to open a window")
    global size
    size = (x, y)
    print "X server size: %d x %d" % (size[0], size[1])
    return(pygame.display.set_mode(size))

def getFb():
    print("Try to open Fb")
    global size
    disp_no = os.getenv("DISPLAY")
    print("disp_no " +str(disp_no))
    if disp_no:
        print "I'm running under X display = {0}".format(disp_no)

    drivers = ['fbcon', 'directfb', 'svgalib', 'xvfb', 'x11', 'dga', 'ggi', 'vgl', 'svgalib', 'aalib', 'windib', 'directx'] #the last 2 are windows where we should not need the fb since it always has desktop, but lets keep them anyway...
    found = False
    for driver in drivers:
        # Make sure that SDL_VIDEODRIVER is set
        if not os.getenv('SDL_VIDEODRIVER'):
            os.putenv('SDL_VIDEODRIVER', driver)
        try:
            print("Driver: "+driver)
            pygame.display.init()
        except pygame.error:
            print 'Driver: {0} failed.'.format(driver)
            continue
        found = True
        print("this one works.")
        break


    if not found:
        raise Exception('No suitable video driver found!')

    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print "Framebuffer size: %d x %d" % (size[0], size[1])
    return(pygame.display.set_mode(size))
