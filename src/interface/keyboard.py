
import errors
import interface

from libs.xdotool import XDoTool

__X_DO_TOOL = None
__ERROR_MESSGE = None

def __keyboard_error():
    if __X_DO_TOOL:
        return False

    return errors.error(errors.KEYBOARD_NOT_INIT)

def input_string(_input_string):
    '''Call XDoTool input_string function'''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_string, (_input_string, ))
    return False # We don't want to return anything

def press_enter():
    ''' Simulate enter keyboard input '''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_single_symbol, (__X_DO_TOOL.SYM_ENTER, ))
    return False # We don't want to return anything

def press_tab():
    ''' Simulate tab keyboard input '''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_single_symbol, (__X_DO_TOOL.SYM_TAB, ))
    return False # We don't want to return anything

def press_backspace():
    ''' Simulate back space keyboard input '''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_single_symbol, (__X_DO_TOOL.SYM_BACKSPACE, ))
    return False # We don't want to return anything

def press_arrow_up():
    ''' Simulate arrow up keyboard input '''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_single_symbol, (__X_DO_TOOL.SYM_ARROW_UP, ))
    return False # We don't want to return anything

def press_arrow_righ():
    ''' Simulate arrow right keyboard input '''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_single_symbol, (__X_DO_TOOL.SYM_ARROW_RIGHT, ))
    return False # We don't want to return anything


def press_arrow_down():
    ''' Simulate arrow down keyboard input '''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_single_symbol, (__X_DO_TOOL.SYM_ARROW_DOWN, ))
    return False # We don't want to return anything


def press_arrow_left():
    ''' Simulate arrow left keyboard input '''
    error = __keyboard_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.input_single_symbol, (__X_DO_TOOL.SYM_ARROW_LEFT, ))
    return False # We don't want to return anything

if __name__ == 'interface.keyboard':
    # XDoTool needs to be initialized when mouse interface is imported
    __X_DO_TOOL = XDoTool()

    __THREAD = interface.InterfaceThread(interface.KEYBOARD_INTERFACE)
    __THREAD.start()
