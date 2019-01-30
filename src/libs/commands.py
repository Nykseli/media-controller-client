'''
System commands
'''
import os
import subprocess
import errors

def os_subprosses_handler(command, error_name) -> dict:
    ''' call subprocess.Popen and return error there is an exception '''
    try:
        subprocess.Popen(command, shell=True, env=os.environ.copy())
    except Exception:
        return errors.error(error_name);

    return None
