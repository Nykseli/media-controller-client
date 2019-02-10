'''
Functions for browser interface
'''

import errors
import interface
from libs.chromiumwrapper import Browser

__BROWSER = None

def __browser_error():
    ''' Return False if no errors '''
    if __BROWSER:
        return False

    return errors.error(errors.BROWSER_NOT_INIT)

def start_browser():
    ''' Call Browser start_browser function '''
    error = __browser_error()
    if error:
        return error

    __THREAD.add_to_queue(__BROWSER.start_browser)
    return False # No error message

def stop_browser():
    ''' Call Browser stop_browser function '''
    error = __browser_error()
    if error:
        return error

    __THREAD.add_to_queue(__BROWSER.stop_browser)
    return False # No error message

if __name__ == 'interface.browser':
    __BROWSER = Browser()

    __THREAD = interface.InterfaceThread(interface.BROWSER_INTERFACE)
    __THREAD.start()
