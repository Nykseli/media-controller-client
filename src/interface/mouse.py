'''
Functions for mouse interface
'''
import interface
from libs.xdotool import XDoTool

__X_DO_TOOL = None
__ERROR_MESSGE = None

def __mouse_error():
    if __X_DO_TOOL:
        return False

    return  {"error": "Mouse not initialized"}

def left_mouse_click():
    '''Call XDoTool left_mouse_click function'''
    error = __mouse_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.left_mouse_click)
    return False # We don't want to return anything

def move_mouse_x(amount):
    '''Call XDoTool move_mouse_x function'''

    error = __mouse_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.move_mouse_x, (amount, ))
    return False # We don't want to return anything

def move_mouse_y(amount):
    '''Call XDoTool move_mouse_y function'''

    error = __mouse_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.move_mouse_y, (amount, ))
    return False # We don't want to return anything

def set_mouse_position(_x, _y):
    '''Call XDoTool set_mouse_position function'''

    error = __mouse_error()
    if error:
        return error

    __THREAD.add_to_queue(__X_DO_TOOL.set_mouse_position, (_x, _y))
    return False # We don't want to return anything


if __name__ == 'interface.mouse':
    # XDoTool needs to be initialized when mouse interface is imported
    __X_DO_TOOL = XDoTool()

    __THREAD = interface.InterfaceThread(interface.MOUSE_INTERFACE)
    __THREAD.start()
