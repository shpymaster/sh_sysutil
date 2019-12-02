""" ------------
module: sh_sysutils
version: 1.1.20191018

Module defines systems utilities.
-------------"""

class shOptionDictionary:
    """
    Creates dictionary from entered agruments (options).
    when separated =1 finds pairs "-x value" in args,
    when separated =0 finds pairs "-xValue" in args,
    names are defined by optid separator,
    returns dictionary like {'-x': 'value1', '-y': 'value2'}
    """
    def __init__(self, optList, optid='-', separated=1):
        self.OptionDict = {}
        while optList:
            if optList[0][0] == optid:
                if (separated):
                    self.OptionDict[optList[0]] = optList[1]
                    optList = optList[2:]
                else:
                    self.OptionDict[optList[0][:2]] = optList[0][2:]
                    optList = optList[1:]
            else:
                optList = optList[1:]

    def set_option_dict(self, newOptDict):
        self.OptionDict = newOptDict

    def get_option(self, key):
        try:
            val = self.OptionDict[key]
        except:
            val = ""
        return val 


class shExeFile:
    """
    Defines .EXE file as an Object. 
    Windows variables %VAR% are expanded for .EXE file.
    Existance of the file may be checked during initialization. 
    In such case Exception FileNotFoundError will be raised if file not found.
    Arguments may be set or changed. Run may be specifies with shell=True option.
    """
    def __init__(self, exeFileName, *exeFileArguments, checkExist=True):
        import os.path
        self.exeFileName = os.path.expandvars(exeFileName)
        if checkExist:
            if not os.path.exists (self.exeFileName):
                raise FileNotFoundError (self.exeFileName)       
        self.arguments = exeFileArguments

    def set_arguments(self, *saArguments):
        self.arguments = saArguments

    def run(self, useShell=False):
        import subprocess
        result = subprocess.run ([self.exeFileName, self.arguments], shell=useShell)
        return result.returncode


def sh_wait_path_availability(pathstring, maxseconds, checkinterval=1):
    """
    Waits accessibility of the defined pathstring.
    If not accessible after maxseconds period, Exception FileNotFoundError will be raised.
    """
    import os.path
    import time
    startsec = time.perf_counter()
    while not os.path.exists(pathstring):
        currentsec = time.perf_counter()
        if (currentsec - startsec) > maxseconds:
            raise FileNotFoundError (pathstring)
        time.sleep(checkinterval)
    return 0


if __name__ == "__main__":
    '''
    self-test deleted
    '''
