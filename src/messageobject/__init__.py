
'''
Server sends back data in following format
{
    "interface": string <name of the interface>,
    "messageData":{
        <Object that contains data defined by api>
    }
}
'''

def get_message_object(interface_name, message_data_object):
    ''' Get message object in format defined by README.md '''
    data_object = {
        "interface": interface_name,
        "messageData": message_data_object
    }

    return data_object
