#!/usr/bin/python3
'''
Wrapper for xdotool program
'''
import time
import subprocess

import errors
import libs.commands as commands

class XDoTool():
    ''' Class that wraps xdotool '''
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

    # Arrow keys
    SYM_ARROW_UP = 'Up'
    SYM_ARROW_RIGHT = 'Right'
    SYM_ARROW_DOWN = 'Down'
    SYM_ARROW_LEFT = 'Left'

    def __init__(self):
        self.window_size = self.get_widow_size()

    def get_widow_size(self):
        ''' Get window size '''
        # TODO:
        return False

    def __char_to_unicode_char_point(self, _c)-> str:
        '''
        Return unicode code point in format that xdotool understands.
        E.g. 'Ä' -> "U00C4"
        '''
        return "U%04X" % ord(_c)

    def get_mouse_position(self):
        ''' return mouse x, y position tuple '''
        result_string = subprocess.check_output(['xdotool', 'getmouselocation'])
        result_array = str(result_string).split()
        print(str(result_array))
        x_pos = result_array[0].split(':')[1]
        y_pos = result_array[1].split(':')[1]
        return (x_pos, y_pos)

    def set_mouse_position(self, _x, _y):
        ''' set mouse to x y position '''
        command_string = "xdotool mousemove {} {}".format(_x, _y)
        print(command_string)
        return commands.os_subprosses_handler(command_string, errors.XDOTOOL_GENERAL)

    def move_mouse_x(self, pixel_amount):
        ''' Move cursor on x axis by pixel_amount. Positive is right, negative is left '''
        if not pixel_amount:
            pixel_amount = 0
        else:
            pixel_amount = int(pixel_amount)

        if pixel_amount < 0:
            command_string = "xdotool mousemove_relative -- {} 0".format(pixel_amount)
        else:
            command_string = "xdotool mousemove_relative {} 0".format(pixel_amount)
        return commands.os_subprosses_handler(command_string, errors.XDOTOOL_GENERAL)

    def move_mouse_y(self, pixel_amount):
        ''' Move cursor on y axis by pixel_amount. Positive amount is down, negative is up '''
        if not pixel_amount:
            pixel_amount = 0
        else:
            pixel_amount = int(pixel_amount)

        if pixel_amount < 0:
            command_string = "xdotool mousemove_relative -- 0 {}".format(pixel_amount)
        else:
            command_string = "xdotool mousemove_relative 0 {}".format(pixel_amount)
        return commands.os_subprosses_handler(command_string, errors.XDOTOOL_GENERAL)


    def left_mouse_click(self):
        ''' Simulate left mouse click'''
        command_string = "xdotool click 1"
        return commands.os_subprosses_handler(command_string, errors.XDOTOOL_GENERAL)

    def __char_to_xdotool_symbol(self, char):
        ''' Change char to a value that xdotool understand'''

        # Get int value of character
        char_val = ord(char)

        # If character is not ascii
        if char_val > 127:
            return self.__char_to_unicode_char_point(char)
        # If character is newLine (\n)
        if char_val == 10:
            return self.SYM_ENTER
        # If character is a space
        if char_val == 32:
            return self.SYM_SPACE
        # If character is !
        if char_val == 33:
            return self.SYM_EXCLAMATION
        # If character is "
        if char_val == 34:
            return self.SYM_DOUBLE_QUOTE
        # If character is #
        if char_val == 35:
            return self.SYM_NUMBER_SIGN
        # If character is $
        if char_val == 36:
            return self.SYM_DOLLAR_SIGN
        # If character is %
        if char_val == 37:
            return self.SYM_PERCENT
        # If character is &
        if char_val == 38:
            return self.SYM_AMBERSAND
        # If charachter if '
        if char_val == 39:
            return self.SYM_APOSTROPHE
        # If character is (
        if char_val == 40:
            return self.SYM_PAREN_LEFT
        # If character is )
        if char_val == 41:
            return self.SYM_PAREN_RIGHT
        # If character is *
        if char_val == 42:
            return self.SYM_ASTERISK
        # If character is +
        if char_val == 43:
            return self.SYM_PLUS
        # If character is ,
        if char_val == 44:
            return self.SYM_COMMA
        # If character is -
        if char_val == 45:
            return self.SYM_MINUS
        # If character is .
        if char_val == 46:
            return self.SYM_PERIOD
        # If character is /
        if char_val == 47:
            return self.SYM_SLASH
        # If character is :
        if char_val == 58:
            return self.SYM_COLON
        # If character is ;
        if char_val == 59:
            return self.SYM_SEMICOLON
        # If character is <
        if char_val == 60:
            return self.SYM_LESSER_THAN
        # If character is =
        if char_val == 61:
            return self.SYM_EQUAL
        # If character is >
        if char_val == 62:
            return self.SYM_GREATER_THAN
        # If character is ?
        if char_val == 63:
            return self.SYM_QUESTION_MARK
        # If character is @
        if char_val == 64:
            return self.SYM_AT
        # If character [
        if char_val == 91:
            return self.SYM_SQUARE_BRACKET_LEFT
        # If character is \
        if char_val == 92:
            return self.SYM_BACKSLASH
        # If character is ]
        if char_val == 93:
            return self.SYM_SQUARE_BRACKET_RIGHT
        # If character is ^
        if char_val == 94:
            return self.SYM_CIRCUMFLEX
        # If character is _
        if char_val == 95:
            return self.SYM_UNDERSCORE
        # IF character is `
        if char_val == 96:
            return self.SYS_GRAVE_ACCENT
        # If character is {
        if char_val == 123:
            return self.SYM_CURLY_BRACKET_LEFT
        # If character is |
        if char_val == 124:
            return self.SYM_BAR
        # If character is }
        if char_val == 125:
            return self.SYM_CURLY_BRACKET_RIGHT
        # If character is ~
        if char_val == 126:
            return self.SYM_TILDE

        # If character is ascii alphabet
        return char

    def input_single_char(self, char):
        '''Change char to a value that xdotool understand and simulate input with it'''
        symbol = self.__char_to_xdotool_symbol(char)
        command_string = "xdotool key --clearmodifiers {}".format(symbol)
        return commands.os_subprosses_handler(command_string, errors.XDOTOOL_GENERAL)

    def input_single_symbol(self, symbol):
        ''' Simulate input with symbol that xdotool understands '''
        command_string = "xdotool key --clearmodifiers {}".format(symbol)
        return commands.os_subprosses_handler(command_string, errors.XDOTOOL_GENERAL)

    def input_string(self, input_string: str):
        ''' Input string to device with simulating keyboard input'''
        for _c in input_string:
            result = self.input_single_char(_c)
            time.sleep(0.05) # Short sleep makes sure that the chars are typed in right order
            if result:
                print(result)
                return result
        return None

    def get_all_windows(self):
        #TODO: get all visible window names
        pass

    def focus_to_window(self, window_name):
        #TODO: focus to ceratin window
        pass
