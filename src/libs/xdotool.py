#!/usr/bin/python3

import os
import subprocess

import errors
import libs.commands as commands

class XDoTool():

    ### xdotool key symbols ###

    # Symbol for enter key
    SYM_ENTER = 'Return'

    # Sybol for backspace key
    SYM_BACKSPACE = 'BackSpace'

    # Symbol for tab key
    SYM_TAB = 'Tab'

    # Symbol for space key
    SYM_SPACE = 'space'

    # Symbol for ( character
    SYM_PAREN_LEFT = 'parenleft'

    # Symbol for ) character
    SYM_PAREN_RIGHT = 'parenright'

    # Symbol for ! character
    SYM_EXCLAMATION = 'exclam'

    # Symbol for ? character
    SYM_QUESTION_MARK = 'question'

    # Symbol for < character
    SYM_LESSER_THAN = 'less'

    # Symbol for > character
    SYM_GREATER_THAN = 'greater'

    # Symbol for = character
    SYM_EQUAL = 'equal'

    # Symbol for @ character
    SYM_AT = 'at'

    # Symbol for " character
    SYM_DOUBLE_QUOTE = 'quotedbl'

    # Symbol for # character
    SYM_NUMBER_SIGN = 'numbersign'

    # Symbol for $ character
    SYM_DOLLAR_SIGN = 'dollar'

    # Symbol for % character
    SYM_PERCENT = 'percent'

    # Symbol for & character
    SYM_AMBERSAND = 'ampersand'

    # Symbol for ' character
    SYM_APOSTROPHE = 'apostrophe'

    # Symbol for [ character
    SYM_SQUARE_BRACKET_LEFT = 'bracketleft'

    # Symbol for ] character
    SYM_SQUARE_BRACKET_RIGHT = 'bracketright'

    # Symbol for { character
    SYM_CURLY_BRACKET_LEFT = 'braceleft'

    # Symbol for } character
    SYM_CURLY_BRACKET_RIGHT = 'braceright'

    # Symbol for * character
    SYM_ASTERISK = 'asterisk'

    # Symbol for ^ character
    SYM_CIRCUMFLEX = 'asciicircum'

    # Symbol for - character
    SYM_MINUS = 'minus'

    # Symbol for ` character
    SYS_GRAVE_ACCENT = 'grave'

    # Symbol for _ character
    SYM_UNDERSCORE = 'underscore'

    # Symbol for + character
    SYM_PLUS = 'plus'

    # Symbol for / character
    SYM_SLASH = 'slash'

    # Symbol for \ character
    SYM_BACKSLASH = 'backslash'

    # Symbol for . character
    SYM_PERIOD = 'period'

    # Symbol for , character
    SYM_COMMA = 'comma'

    # Symbol for : character
    SYM_COLON = 'colon'

    # Symbol for ; character
    SYM_SEMICOLON = 'semicolon'

    # Symbol for ~ character
    SYM_TILDE = 'asciitilde'

    # Symbol for | character
    SYM_BAR = 'bar'

    def __init__(self):
        self.getWindowSize = self.getWindowSize()
        pass

    def getWindowSize(self):
        pass

    def __charToUnicodeCodePoint(self, c)-> str:
        '''
        Return unicode code point in format that xdotool understands.
        E.g. 'Ä' -> "U00C4"
        '''
        return "U%04X" % ord(c)

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
        return commands.osSystemHanlder(command_string, errors.XDOTOOL_GENERAL)

    def moveMouseX(self, pixel_amount):
        if not pixel_amount:
            pixel_amount = 0
        else:
            pixel_amount = int(pixel_amount)

        if(pixel_amount < 0):
            command_string = "xdotool mousemove_relative -- {} 0".format(pixel_amount)
        else:
            command_string = "xdotool mousemove_relative {} 0".format(pixel_amount)
        return commands.osSystemHanlder(command_string, errors.XDOTOOL_GENERAL)

    def moveMouseY(self, pixel_amount):
        if not pixel_amount:
            pixel_amount = 0
        else:
            pixel_amount = int(pixel_amount)

        if(pixel_amount < 0):
            command_string = "xdotool mousemove_relative -- 0 {}".format(pixel_amount)
        else:
            command_string = "xdotool mousemove_relative 0 {}".format(pixel_amount)
        return commands.osSystemHanlder(command_string, errors.XDOTOOL_GENERAL)


    def leftMouseClick(self):
        command_string = "xdotool click 1"
        return commands.osSystemHanlder(command_string, errors.XDOTOOL_GENERAL)

    def __charToXdotoolSymbol(self, char):
        ''' Change char to a value that xdotool understand'''

        # Get int value of character
        charVal = ord(char)
        print(str(charVal == 10))
        # If character is not ascii
        if charVal > 127:
            return self.__charToUnicodeCodePoint(char)
        # If character is newLine (\n)
        elif charVal == 10:
            return self.SYM_ENTER
        # If character is a space
        elif charVal == 32:
            return self.SYM_SPACE
        # If character is !
        elif charVal == 33:
            return self.SYM_EXCLAMATION
        # If character is "
        elif charVal == 34:
            return self.SYM_DOUBLE_QUOTE
        # If character is #
        elif charVal == 35:
            return self.SYM_NUMBER_SIGN
        # If character is $
        elif charVal == 36:
            return self.SYM_DOLLAR_SIGN
        # If character is %
        elif charVal == 37:
            return self.SYM_PERCENT
        # If character is &
        elif charVal == 38:
            return self.SYM_AMBERSAND
        # If charachter if '
        elif charVal == 39:
            return self.SYM_APOSTROPHE
        # If character is (
        elif charVal == 40:
            return self.SYM_PAREN_LEFT
        # If character is )
        elif charVal == 41:
            return self.SYM_PAREN_RIGHT
        # If character is *
        elif charVal == 42:
            return self.SYM_ASTERISK
        # If character is +
        elif charVal == 43:
            return self.SYM_PLUS
        # If character is ,
        elif charVal == 44:
            return self.SYM_COMMA
        # If character is -
        elif charVal == 45:
            return self.SYM_MINUS
        # If character is .
        elif charVal == 46:
            return self.SYM_PERIOD
        # If character is /
        elif charVal == 47:
            return self.SYM_SLASH
        # If character is :
        elif charVal == 58:
            return self.SYM_COLON
        # If character is ;
        elif charVal == 59:
            return self.SYM_SEMICOLON
        # If character is <
        elif charVal == 60:
            return self.SYM_LESSER_THAN
        # If character is =
        elif charVal == 61:
            return self.SYM_EQUAL
        # If character is >
        elif charVal == 62:
            return self.SYM_GREATER_THAN
        # If character is ?
        elif charVal == 63:
            return self.SYM_QUESTION_MARK
        # If character is @
        elif charVal == 64:
            return self.SYM_AT
        # If character [
        elif charVal == 91:
            return self.SYM_SQUARE_BRACKET_LEFT
        # If character is \
        elif charVal == 92:
            return self.SYM_BACKSLASH
        # If character is ]
        elif charVal == 93:
            return self.SYM_SQUARE_BRACKET_RIGHT
        # If character is ^
        elif charVal == 94:
            return self.SYM_CIRCUMFLEX
        # If character is _
        elif charVal == 95:
            return self.SYM_UNDERSCORE
        # IF character is `
        elif charVal == 96:
            return self.SYS_GRAVE_ACCENT
        # If character is {
        elif charVal == 123:
            return self.SYM_CURLY_BRACKET_LEFT
        # If character is |
        elif charVal == 124:
            return self.SYM_BAR
        # If character is }
        elif charVal == 125:
            return self.SYM_CURLY_BRACKET_RIGHT
        # If character is ~
        elif charVal == 126:
            return self.SYM_TILDE

        # If character is ascii alphabet
        return char

    def inputSingleChar(self, c):
        '''Change char to a value that xdotool understand and simulate input with it'''
        symbol = self.__charToXdotoolSymbol(c)
        print(str(symbol))
        commandString = "xdotool key --clearmodifiers {}".format(symbol)
        print(str(commandString))
        return commands.osSystemHanlder(commandString, errors.XDOTOOL_GENERAL)

    def inputSingleSymbol(self, symbol):
        import time
        time.sleep(3)

        ''' Simulate input with symbol that xdotool understands '''
        commandString = "xdotool key --clearmodifiers {}".format(symbol)
        return commands.osSystemHanlder(commandString, errors.XDOTOOL_GENERAL)

    def inputString(self, inputString: str):
        import time
        time.sleep(3)

        ''' Input string to device with simulating keyboard input'''
        for c in inputString:
            result = self.inputSingleChar(c)
            if result:
                return result

    def getAllWindows(self):
        #TODO: get all visible window names
        pass

    def focusToWindow(self, window_name):
        #TODO: focus to ceratin window
        pass


