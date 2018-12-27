#!/usr/bin/python3

import os
import subprocess

class XDoTool():

    def __init__(self):
        self.getWindowSize = self.getWindowSize()
        pass

    def getWindowSize(self):
        pass

    def getMousePosition(self):
        result_string = subprocess.check_output(['xdotool', 'getmouselocation'])
        result_array = str(result_string).split()
        print(str(result_array))
        x_pos = result_array[0].split(':')[1]
        y_pos = result_array[1].split(':')[1]
        return (x_pos, y_pos)
        pass

    def setMousePosition(self, x, y):
        command_string = "xdotool mousemove {} {}".format(x, y)
        print(command_string)
        os.system(command_string)
        pass

    def moveMouseX(self, pixel_amount):
        if not pixel_amount:
            pixel_amount = 0
        else:
            pixel_amount = int(pixel_amount)

        if(pixel_amount < 0):
            command_string = "xdotool mousemove_relative -- {} 0".format(pixel_amount)
        else:
            command_string = "xdotool mousemove_relative {} 0".format(pixel_amount)
        os.system(command_string)

    def moveMouseY(self, pixel_amount):
        if not pixel_amount:
            pixel_amount = 0
        else:
            pixel_amount = int(pixel_amount)

        if(pixel_amount < 0):
            command_string = "xdotool mousemove_relative -- 0 {}".format(pixel_amount)
        else:
            command_string = "xdotool mousemove_relative 0 {}".format(pixel_amount)
        os.system(command_string)

    def leftMouseClick(self):
        command_string = "xdotool click 1"
        os.system(command_string)

    def getAllWindows(self):
        #TODO: get all visible window names
        pass

    def focusToWindow(self, window_name):
        #TODO: focus to ceratin window
        pass


