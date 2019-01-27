import os
import errors
import subprocess

def osSystemHanlder(command, errorName) -> dict:
    try:
        subprocess.Popen(command, shell=True, env=os.environ.copy())
    except Exception:
        return errors.error(errorName);
        pass

    return None
