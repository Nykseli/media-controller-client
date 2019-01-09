
import errors

from libs.xdotool import XDoTool

__X_DO_TOOL = None
__ERROR_MESSGE = None

def __isKeyboardUsable():
    if __X_DO_TOOL:
        return True
    else:
        __ERROR_MESSGE = errors.error(errors.KEYBOARD_NOT_INIT)
    return False

def inputString(inputString):
    '''Call XDoTool inputString function'''
    if not __isKeyboardUsable():
        return __ERROR_MESSGE

    __X_DO_TOOL.inputString(inputString)

def pressEnter():
    ''' Simulate enter keyboard input '''
    if not __isKeyboardUsable():
        return __ERROR_MESSGE

    __X_DO_TOOL.inputSingleSymbol(__X_DO_TOOL.SYM_ENTER)

def pressTab():
    ''' Simulate tab keyboard input '''
    if not __isKeyboardUsable():
        return __ERROR_MESSGE

    __X_DO_TOOL.inputSingleSymbol(__X_DO_TOOL.SYM_TAB)

def pressBackSpace():
    ''' Simulate back space keyboard input '''
    if not __isKeyboardUsable():
        return __ERROR_MESSGE

    __X_DO_TOOL.inputSingleSymbol(__X_DO_TOOL.SYM_BACKSPACE)

if __name__ == 'interface.keyboard':
    # XDoTool needs to be initialized when mouse interface is imported
    __X_DO_TOOL = XDoTool()
