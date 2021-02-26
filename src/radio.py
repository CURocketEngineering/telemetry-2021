"""Low level comm implementation."""

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import serial.tools.list_ports as prtlst
import sys
from time import time as unixtimestamp
from json import loads, dumps

from copy import deepcopy

class Antenna:
    def __init__(
            self,
            port="",
            remote_address="",
            verbose=False
    ):
        self.verbose = verbose
        if port == "":
            port = self.find_port()
        self.port = port
        self.verbose_print(f"Port: {self.port}")

        self.last_time_sent = 0

        if self.port != "" and remote_address != "":
            self.device = XBeeDevice(self.port, 9600)
            self.active = True
            self.has_remote = True

            try:
                self.device.open()
            except Exception as e:
                print(e)
                self.active = False
            try:
                add_64 = (XBee64BitAddress.from_hex_string(
                    remote_address
                ))
                self.remote_device = RemoteXBeeDevice(self.device, add_64)
            except Exception as e:
                self.has_remote = False
                print("Error on remote device: ", e)
        else:
            self.active = False
            self.device = None

        self.ready_data = {}
        self.cur_data = {}
        self.cur_uts = 0

    def find_port(self):
        ports = prtlst.comports()
        for port in ports:
            try:
                if "FTDI" in port.manufacturer:
                    return port.device
            except Exception:
                pass
        return ""

    def send(
            self,
            data,
            time=None,
            data_key=None,
            skip_time=0,
             parent="",
            as_json=False
    ):
        """
        Recursively send asynchronous data.
        """
        if as_json:
            data = loads(data)
        # Update Time
        if time == None:
            time = unixtimestamp()
            #self.last_time_sent = time
            # Skip if time buffer too low
            if skip_time != 0:
                if time - self.last_time_sent < skip_time:
                    return None
            self.last_time_sent = time

        self.verbose_print((self.active, data))
        if self.active:
            try:
                if type(data) == dict:
                    for key in data:
                        parent = "" if data_key == None else data_key
                        self.send(
                            data[key], time=time,
                            data_key=key, parent=parent
                        )
                else:
                    send_data = {
                        "uts" : time,
                        f"{parent}_{str(data_key)}" : data
                    }
                    to_send = dumps(send_data).encode()
                    self.verbose_print(to_send)
                    self.device.send_data_async(
                        self.remote_device,
                        to_send
                    )
            except Exception as e:
                self.verbose_print(f"COULDN'T SEND {data}, ERROR {e}")
        return None

    def verbose_print(self, message):
        if self.verbose:
            print(message)

    def read_time(self, time):
        if not self.active:
            print("NOT ACTIVE")
            return "{}"
        new_data = self.device.read_data(time)
        try:
            new_data_processed = loads(new_data.data.decode())
        except Exception as e:
            print(e)
            return
        key_name = ""
        val = 0
        for key in new_data_processed:
            if "uts" in key:
                self.cur_uts = new_data_processed[key]
            else:
                key_name = key
                val = new_data_processed[key]
        if self.cur_uts in self.cur_data:
            self.cur_data[self.cur_uts][key_name] = val
        if self.cur_uts not in self.cur_data:
            self.ready_data.update(self.cur_data)
            self.cur_data = {
                self.cur_uts: {
                    key_name: val
                }
            }

    def send_halt(self):
        return

    def send_arm(self):
        return

    def start_sim(self):
        return

    def get_finished_data(self):
        finished_data = deepcopy(self.ready_data)
        if finished_data == {}:
            return {}
        self.ready_data = {}
        if "_time" in finished_data:
            finished_data["time"] = finished_data["_time"]
        finished_data["sensors"] = {"gyro": {}}
        finished_data["sensors"]["alt"] = finished_data.get("sensors_alt", 0)
        for i in ["x", "y", "z"]:
            finished_data["sensors"]["gyro"][i] = finished_data.get(f"gyro_{i}", 0)
        return finished_data

#ant = Antenna(remote_address="0013A20041957215", verbose=True)
#ant = Antenna(remote_address="0013A2004195721E", verbose=True)
