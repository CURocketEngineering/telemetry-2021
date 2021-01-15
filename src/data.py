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
should_kill_thread = False

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
        self.has_finished = False


    def get_data(self, empty=True):
        r_data = {}
        try:
            self.data_lock.acquire()
            r_data = self.data.copy()
            if empty:
                self.data = deepcopy(empty_data)
        finally:
            self.data_lock.release()
        return r_data

    def update_data(self):
        if self.has_finished:
            return
        if not self.use_comm and self.is_sim:
            try:
                self.data_lock.acquire()
                new_dt = datetime.now()
                if (new_dt - self.last_dt).seconds >= SIM_DT:
                    self.last_dt = new_dt
                    newline = self._f.readline()
                    if newline != "":
                        newjson = loads(self._f.readline())
                        self.update_readings_from_dict(newjson)
                    else:
                        self.has_finished = True
            finally:
                self.data_lock.release()
        elif not self.use_comm and not self.is_sim:
            try:
                self.data_lock.acquire()
                for line in self._f.readlines():
                    newjson = loads(line)
                    self.update_readings_from_dict(newjson)
                self.has_finished = True
            finally:
                self.data_lock.release()
        # TODO else
        return

    def update_readings_from_dict(self, newjson):
        self.data["sensors"]["gyro"]["x"].append(newjson["sensors"]["gyro"]["x"])
        self.data["sensors"]["gyro"]["y"].append(newjson["sensors"]["gyro"]["y"])
        self.data["sensors"]["gyro"]["z"].append(newjson["sensors"]["gyro"]["z"])
        self.data["sensors"]["alt"].append(newjson["sensors"]["alt"])
        self.data["time"].append(newjson["time"])

def update_data(dataobj):
    global should_kill_thread
    while True:
        dataobj.update_data()
        if should_kill_thread:
            should_kill_thread = False
            return
