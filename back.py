from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
from hashing_utilities import md5, sha1, sha256

class CheckEvent:
    def __init__(self, filename, method, _hash):
        self.hash_input = _hash
        self.fname = filename
        self.methodname = method

class HashCalc(QObject):

    trigger_calculated = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.trigger_calculated.connect(parent.display_result)
        self.methods = {"sha1": sha1, "md5": md5, "sha256": sha256}

    @staticmethod
    def days_hours_minutes(td): # Transform timedelta object to minutes and seconds
        values = ((td.seconds//60)%60, td.seconds)
        return f"{values[0]} minutes, {values[1]} seconds"


    def checksum(self, event):
        """
        Given a path(filename) and a hash algorhitm(_hash)
        returns the human-readable hash value of the file.
        """
        method = self.methods[event.methodname]
        print("Method to use: ", method)
        print("Path: ", event.fname)
        print("User hash: ", event.hash_input)
        print("Calculando!")
        try:
            t_0 = datetime.now()
            _bool = event.hash_input == method(event.fname)
            delta = datetime.now() - t_0
            print("Runtime: {}".format(HashCalc.days_hours_minutes(delta)))
            self.trigger_calculated.emit(_bool)
        except FileNotFoundError:
            print("The file given by the path does not exist")

