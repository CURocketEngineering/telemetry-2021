from json import loads
from datetime import datetime
from threading import Lock, Thread
from copy import deepcopy

from . import radio

DATAFILE = "uploads/sim_irec2019.json"
SIM_DT = .02

kill_radio = False

# TODO, read and send more data types
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
thread_should_die = False

class DataHandler:
    """
    DataHandler generalizes file io and radio connections for the sake of
    keeping application.py sane. 
    """
    def __init__(self, use_comm : bool, filename=DATAFILE, is_sim=False):
        self.use_comm = use_comm
        self.is_sim = is_sim
        self._f = None
        self.radio = None
        if use_comm:
            self.radio = radio.Antenna(remote_address="0013A20041957215")
            # remot_address will need to be changed with different radios,
            # this should be moved to the gui
        else:
            self._f = open(filename, "r")
        self.data = deepcopy(empty_data)
        self.data_lock = Lock()  # Necessary for the sake of multi-threading
        self.last_dt = datetime.now()
        self.has_finished = False

    def get_data(self, empty=True) -> dict:
        """
        Returns a dictionary of data. 
        If empty=True, the old data is emptied out and removed (so it won't
        be returned next time).
        """
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
        """
        Updates self.data with the newest data depending on initialization
        flags.
        """
        # If the data collection has been finished (eof, radio died, etc.), return
        if self.has_finished:
            return
        # If data is from a file and its a simulation, update the file data with
        # the next lines of data
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
        # If data is from a file and its not a simulation, dump all data and finish
        elif not self.use_comm and not self.is_sim:
            try:
                self.data_lock.acquire()
                for line in self._f.readlines():
                    newjson = loads(line)
                    self.update_readings_from_dict(newjson)
                self.has_finished = True
            finally:
                self.data_lock.release()
        # If data is from comm, simulation or not, read in data that has been completed
        elif self.use_comm:
            #self.update_readings_from_dict(self.radio.get_finished_data())
            #self.radio.read_time(1000)
            try:
                self.data_lock.acquire()
                d = self.radio.get_finished_data()
                if d:
                    self.update_readings_from_dict(d)
            except Exception as e:
                print("ERROR", e)  # Error likely timeout
            finally:
                self.data_lock.release()
        else:
            pass
        return

    def update_readings_from_dict(self, newjson):
        """
        Update self.data with a dictionary of new data.
        TODO: this should be expanded to include more data.
        """
        self.data["sensors"]["gyro"]["x"].append(newjson["sensors"]["gyro"]["x"])
        self.data["sensors"]["gyro"]["y"].append(newjson["sensors"]["gyro"]["y"])
        self.data["sensors"]["gyro"]["z"].append(newjson["sensors"]["gyro"]["z"])
        self.data["sensors"]["alt"].append(newjson["sensors"]["alt"])
        self.data["time"].append(newjson["time"])

    def halt(self):
        if self.radio:
            self.radio.send_halt()

    def arm(self):
        if self.radio:
            self.radio.send_arm()

    def eject1(self):
        if self.radio:
            self.radio.send_eject(1)

    def eject2(self):
        if self.radio:
            self.radio.send_eject(2)

    def resume(self):
        return

    def demo_simluation(self):
        return


def update_data(dataobj):
    """
    Ran in a thread to update data independent of application.py
    or the rest of the web app.
    If the bool flag `thread_should_die` is True, update_data kills
    itself. 
    """
    global thread_should_die
    global kill_radio
    if dataobj.use_comm:
        update_radio_thread = Thread(target=radio_update, args=(dataobj,))
        update_radio_thread.daemon = True
        update_radio_thread.start()
    while True:
        dataobj.update_data()
        if thread_should_die:
            thread_should_die = False
            if dataobj.use_comm:
                kill_radio = True
            return

def radio_update(dataobj):
    """
    Used to ping the radio independently of the data update loop.
    """
    global kill_radio
    while True:
        try:
            dataobj.data_lock.acquire()
            dataobj.radio.read_time(0)  # Time is in seconds!
        except Exception as e:
            # Error is likely a read_time (read_data) timeout
            pass
        finally:
            dataobj.data_lock.release()
        if kill_radio:
            print("Radio killed")
            kill_radio = False
            return
