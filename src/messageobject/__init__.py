
'''
Server sends back data in following format
{
    "interface": string <name of the interface>,
    "messageData":{
        <Object that contains data defined by api>
    }
}
'''

def getMessageObject(interfaceName, messageDataObject):
    dataObject = {
        "interface": interfaceName,
        "messageData": messageDataObject
    }

    return dataObject
