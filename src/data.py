from json import loads
from datetime import datetime
from threading import Lock
from copy import deepcopy

DATAFILE = "test/data/sim_irec2019.json"
SIM_DT = .25

empty_data = {
    "sensors": {
        "gyro": {
            "x": [],
            "y": [],
            "z": []
        },
        "alt": []
    },
    "time": []
}


class DataHandler:
    def __init__(self, use_comm : bool, filename=DATAFILE, is_sim=False):
        self.use_comm = use_comm
        self.is_sim = is_sim
        self._f = None
        if use_comm:
            pass
        else:
            self._f = open(filename, "r")
        self.data = deepcopy(empty_data)
        self.data_lock = Lock()
        self.last_dt = datetime.now()


    def get_data(self, empty=True):
        r_data = {}
        try:
            self.data_lock.acquire()
            if self.is_sim:
                r_data = self.data.copy()
                if empty:
                    print("emptying")
                    self.data = deepcopy(empty_data)
            else:
                # TODO else
                pass
        finally:
            self.data_lock.release()
        return r_data

    def update_data(self):
        if not self.use_comm and self.is_sim:
            try:
                self.data_lock.acquire()
                new_dt = datetime.now()
                if (new_dt - self.last_dt).seconds >= SIM_DT:
                    self.last_dt = new_dt
                    newjson = loads(self._f.readline())
                    self.data["sensors"]["gyro"]["x"].append(newjson["sensors"]["gyro"]["x"])
                    self.data["sensors"]["gyro"]["y"].append(newjson["sensors"]["gyro"]["y"])
                    self.data["sensors"]["gyro"]["z"].append(newjson["sensors"]["gyro"]["z"])
                    self.data["sensors"]["alt"].append(newjson["sensors"]["alt"])
                    self.data["time"].append(newjson["time"])
            finally:
                self.data_lock.release()
        # TODO else
        return

def update_data(dataobj):
    while True:
        dataobj.update_data()
