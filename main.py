#!/usr/bin/env python3

# Volumio API
TOGGLE_PLAY_PAUSE_URL = "http://localhost:3000/api/v1/commands/?cmd=toggle"
STOP_URL = "http://localhost:3000/api/v1/commands/?cmd=stop"
PREVIOUS_URL = "http://localhost:3000/api/v1/commands/?cmd=prev"
NEXT_URL = "http://localhost:3000/api/v1/commands/?cmd=next"
GET_STATE_URL = "http://localhost:3000/api/v1/getState"
REPLACE_AND_PLAY_URL = "http://localhost:3000/api/v1/replaceAndPlay"

# Playback Control Tags
TOGGLE_PLAY_PAUSE_ID =
STOP_ID =
PREVIOUS_ID =
NEXT_ID =

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv
import request
import json

reader = SimpleMFRC522()

csv_file = csv.DictReader(open("playback.csv", mode="r"))

last_id = None

def play(id):
    service, uri = search(id)
    if service and uri:
        print("Play", uri)
        headers = { "content-type": "application/json" }
        payload = { "service": service, "uri": uri }
        req = request.post(REPLACE_AND_PLAY_URL, headers=headers, data=json.dumps(payload))
        return
        print(req.text)
        req = request.get(GET_STATE_URL)
        print(req.text)
    else:
        print("New Tag Detected", id)
        print("Please add this tag to `media.csv` file")

def search(id):
    for row in csv_file:
        if id == row["ID"]:
            return row["Service"], row["URI"]
        else:
            return None

#------------------------------------------------------------------------------#

try:
    print("Ready to scan tag...")
    while True:
        id = reader.read_id_no_block()
        if id:
            if id == last_id:
                continue

            last_id = id
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
                play(id)

            try:
                request.get(url, timeout=0.1)
            except:
                pass
        else:
            if not last_id:
                continue

            last_id = None

finally:
    GPIO.cleanup()