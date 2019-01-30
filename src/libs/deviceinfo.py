'''
Functions for getting information about the device
'''
import subprocess
#import socket
#import urllib
#import json

def get_local_ip():
    ''' Get ipv4 address of the local network '''
    ## More portable solution  that doesn't work with vpn ##
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.connect(("8.8.8.8", 80))
    #print(s.getsockname()[0])
    #s.close()
    ############################
    ipadrr = subprocess.check_output("ip route | tail -1 | awk '{print $9}'", shell=True)
    return ipadrr.decode().replace("\n", "")

def get_public_ip():
    ''' Get netwoks public ipv4'''
    #TODO: Do this properly
    return None
