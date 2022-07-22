#!/usr/bin/env python3

import configparser
import csv
import json
import requests
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

env = configparser.ConfigParser()
env.read("/home/volumio/rfid-volumio/.env")

reader = SimpleMFRC522()

# Volumio API
TOGGLE_PLAY_PAUSE_URL = "http://localhost:3000/api/v1/commands/?cmd=toggle"
STOP_URL = "http://localhost:3000/api/v1/commands/?cmd=stop"
PREVIOUS_URL = "http://localhost:3000/api/v1/commands/?cmd=prev"
NEXT_URL = "http://localhost:3000/api/v1/commands/?cmd=next"
GET_STATE_URL = "http://localhost:3000/api/v1/getState"
REPLACE_AND_PLAY_URL = "http://localhost:3000/api/v1/replaceAndPlay"

# Playback Control Tags
TOGGLE_PLAY_PAUSE_ID = env["Control"]["TOGGLE_PLAY_PAUSE_ID"]
STOP_ID = env["Control"]["STOP_ID"]
PREVIOUS_ID = env["Control"]["PREVIOUS_ID"]
NEXT_ID = env["Control"]["NEXT_ID"]

last_id = None


def search(id):
    with open("playback.csv", "r") as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row["ID"] == id:
                return row["Service"], row["URI"]


def play(id):
    if search(id):
        service, uri = search(id)
        print("Play", uri)
        headers = {"content-type": "application/json"}
        payload = {"service": service, "uri": uri}
        requests.post(REPLACE_AND_PLAY_URL,
                      headers=headers, data=json.dumps(payload))
    else:
        newTag(id)


def newTag(id):
    print("New Tag Detected:", id)
    print("Please add this tag to `playback.csv` file")


#------------------------------------------------------------------------------#


try:
    print("Ready to scan tag...")
    while True:
        id = str(reader.read_id())
        if id:
            if id == last_id:
                continue

            print("Tag", id)

            if id == TOGGLE_PLAY_PAUSE_ID:
                print("Play/Pause")
                url = TOGGLE_PLAY_PAUSE_URL
            elif id == STOP_ID:
                print("Stop")
                url = STOP_URL
            elif id == PREVIOUS_ID:
                print("Previous")
                url = PREVIOUS_URL
            elif id == NEXT_ID:
                print("Next")
                url = NEXT_URL
            else:
                last_id = id
                play(id)

            try:
                if url:
                    requests.get(url, timeout=0.1)
                    time.sleep(2.5)
            except:
                pass
        else:
            if not last_id:
                continue

            last_id = None

finally:
    GPIO.cleanup()
