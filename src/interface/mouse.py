from libs.xdotool import XDoTool

__X_DO_TOOL = None
__ERROR_MESSGE = None

def __isMouseUsable():
    if __X_DO_TOOL:
        return True
    else:
        __ERROR_MESSGE = {"error": "Mouse not initialized"}
    return False

def leftMouseClick():
    '''Call XDoTool leftMouseClick function'''
    if not __isMouseUsable():
        return __ERROR_MESSGE

    return __X_DO_TOOL.leftMouseClick()

def moveMouseX(amount):
    '''Call XDoTool moveMouseX function'''

    if not __isMouseUsable():
        return __ERROR_MESSGE

    return __X_DO_TOOL.moveMouseX(amount)

def moveMouseY(amount):
    '''Call XDoTool moveMouseY function'''

    if not __isMouseUsable():
        return __ERROR_MESSGE

    return __X_DO_TOOL.moveMouseY(amount)

def setMousePosition(x, y):
    '''Call XDoTool setMousePosition function'''

    if not __isMouseUsable():
        return __ERROR_MESSGE

    return __X_DO_TOOL.setMousePosition(x, y)


if __name__ == 'interface.mouse':
    # XDoTool needs to be initialized when mouse interface is imported
    __X_DO_TOOL = XDoTool()
