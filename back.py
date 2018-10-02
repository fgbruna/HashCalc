from datetime import datetime
from time import process_time_ns
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

    def checksum(self, event):
        """
        Given a path(filename) and a hash algorhitm(_hash)
        returns the human-readable hash value of the file.
        """
        method = self.methods[event.methodname]
        print("Method to use: ", method)
        print("Path: ", event.fname)
        print("User hash: ", event.hash_input)
        print("Calculating hash!")
        try:
            t_0 = process_time_ns()
            result = method(event.fname).upper()
            _bool = event.hash_input == result
            print(f'Program hash: {result}')
            print("Runtime: {} seconds".format((process_time_ns()-t_0)/1e9))
            self.trigger_calculated.emit(_bool)
        except FileNotFoundError:
            print("The file given by the path does not exist")
