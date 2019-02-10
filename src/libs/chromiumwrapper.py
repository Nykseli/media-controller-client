'''
Wrapper for chromium/chome browser for controlling netflix
'''

import subprocess

class Browser():
    ''' Class wrapper for the browser process '''

    def __init__(self):
        self.browser = None
        # Commands and arguments to start up the browser
        self.cmd_args = []
        self.parse_arguments()

    def parse_arguments(self):
        ''' Create list of arguments that are used to start the browser '''
        #TODO: get this from config.json

        self.cmd_args = [
            'google-chrome',
            'https://netflix.com',
            #'--load-extension=netflix-extension'
        ]

    def start_browser(self):
        ''' Start the browser process '''
        self.browser = subprocess.Popen(self.cmd_args)

    def stop_browser(self):
        ''' Terminate the browser process '''
        self.browser.terminate() # Terminate is more gentle than kill
