#!/bin/bash
source telemetry-env/bin/activate
sleep 2 && firefox 127.0.0.1:5000 &
sudo python application.py
deactivate
