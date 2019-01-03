import os
import errors

def osSystemHanlder(command, errorName) -> dict:
    try:
        os.system(command)
    except Exception:
        return errors.error(errorName);
        pass

    return None
