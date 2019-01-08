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
    # iv = decodeIV(iv)
    # chipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    # messageString = __addPadding(messageString)
    # msg = chipher.encrypt(messageString)
    # msg = base64.b64encode(msg)
    # print(type(msg))
    # print(str(msg))
    #iv = decodeIV(generateRandomIV())
    iv = generateRandomIV()
    chipher = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    messageString = __addPadding(messageString)
    #print(str(len(messageString) % 16))
    msg = chipher.encrypt(messageString)
    msg = base64.b64encode(iv + msg)
    return msg

# def cryptMessageECB(key, messageString):
#     messageString = decodeIV(messageString)
#     chipher = AES.new(key, AES.MODE_ECB, segment_size=128)
#     msg = chipher.encrypt(messageString)
#     print(str(len(msg)))
#     return msg

def decryptMessageCFB(key, cryptMessage):
    #print(str(len(cryptMessage)))
    cryptMessage = base64.b64decode(cryptMessage)
    iv = cryptMessage[:IV_LENGTH]
    dechiper = AES.new(key, AES.MODE_CFB, iv, segment_size=128)
    msg = dechiper.decrypt(cryptMessage[IV_LENGTH:])
    msg = __removePadding(msg)
    #print(msg)
    return msg

# def decryptMessageECB(cryptMessage):
#     print(str(len(cryptMessage)))
#     dechiper = AES.new(KEY, AES.MODE_ECB)
#     msg = dechiper.decrypt(cryptMessage)
#     return msg

# def decodeIV(iv):
#     return base64.b64decode(iv)

# import random, string

# def randomword(length):
#    letters = string.ascii_lowercase
#    return ''.join(random.choice(letters) for i in range(length))

def generateRandomIV():
    # randomList = bytearray(os.urandom(IV_LENGTH))
    # for i in range(len(randomList)):
    #     randomList[i] = int(randomList[i]) % 128

    # return bytes(randomList)
    #random_bytes = os.urandom(IV_LENGTH)
    #return base64.b64encode(random_bytes)#.decode('utf-8')
    return os.urandom(IV_LENGTH)
