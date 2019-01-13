import os
from Crypto.Cipher import AES
import base64

# Define variable for iv length since it always needs to be 16
IV_LENGTH = 16

def __addPadding(message):
    # # Getting length from utf-8 byte array gives us the real length
    # Python can interpret string chars as length one but in reality their length is bigger
    # e.g. Chinese characters
    paddingAmount = IV_LENGTH - (len(bytearray(message, 'utf-8')) % IV_LENGTH)

    for i in range(paddingAmount):
        message += "0"
    return message

def __removePadding(message):
    ''' Remove extra 0 chars from message '''
    messageLength = len(message)
    trimAmount = 0;

    for i in range(messageLength):
        if message[messageLength - 1 - i] == ord('0'):
            trimAmount -= 1
        else:
            break

    if trimAmount < 0:
        return message[:trimAmount]
    else:
        return message

def cryptMessageCFB(key, messageString):
    ''' Generate byte array that contains base64 endcode of iv and crypted message with padding '''
    iv = generateRandomIV()
    chipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    messageString = __addPadding(messageString)
    msg = chipher.encrypt(messageString)
    # Add iv to start of the message so its easy to find
    msg = base64.b64encode(iv + msg)
    return msg


def decryptMessageCFB(key, cryptMessage):
    ''' Decrypt message and remove iv and padding '''
    cryptMessage = base64.b64decode(cryptMessage)
    # IV is the first 16 bytes of the message
    iv = cryptMessage[:IV_LENGTH]
    dechiper = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    # The crypted message is After the 16 bytes
    msg = dechiper.decrypt(cryptMessage[IV_LENGTH:])
    msg = __removePadding(msg)
    return msg

def generateRandomIV():
    return os.urandom(IV_LENGTH)
