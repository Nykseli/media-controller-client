'''
Functions for encrypting and decrypting messages
'''

import os
import base64
from Crypto.Cipher import AES

# Define variable for iv length since it always needs to be 16
IV_LENGTH = 16

def __add_padding(message):
    ''' add '0' to message until message length is dividable by IV_LENGTH '''
    # # Getting length from utf-8 byte array gives us the real length
    # Python can interpret string chars as length one but in reality their length is bigger
    # e.g. Chinese characters
    padding_amount = IV_LENGTH - (len(bytearray(message, 'utf-8')) % IV_LENGTH)

    message += ("0" * padding_amount)
    return message

def __remove_padding(message):
    ''' Remove extra 0 chars from message '''
    message_length = len(message)
    trim_amount = 0

    for i in range(message_length):
        if message[message_length - 1 - i] == ord('0'):
            trim_amount -= 1
        else:
            break

    if trim_amount < 0:
        return message[:trim_amount]

    return message

def encrypt_message_cfb(key, message_string):
    ''' Generate byte array that contains base64 endcode of iv and crypted message with padding '''
    _iv = generate_random_iv()
    chipher = AES.new(key, AES.MODE_CFB, _iv, segment_size=128)
    message_string = __add_padding(message_string)
    msg = chipher.encrypt(message_string)
    # Add iv to start of the message so its easy to find
    msg = base64.b64encode(_iv + msg)
    return msg


def decrypt_message_cfb(key, encrypted_message):
    ''' Decrypt message and remove iv and padding '''
    encrypted_message = base64.b64decode(encrypted_message)
    # IV is the first 16 bytes of the message
    _iv = encrypted_message[:IV_LENGTH]
    dechiper = AES.new(key, AES.MODE_CFB, _iv, segment_size=128)
    # The crypted message is After the 16 bytes
    msg = dechiper.decrypt(encrypted_message[IV_LENGTH:])
    msg = __remove_padding(msg)
    return msg

def generate_random_iv():
    ''' generate random bits that can be used as a iv '''
    return os.urandom(IV_LENGTH)
