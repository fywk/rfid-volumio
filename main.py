#!/usr/bin/env python3

import csv
import json
import requests
import RPi.GPIO as GPIO
import os
import sys
import time
from dotenv import load_dotenv
from mfrc522 import SimpleMFRC522
from pathlib import Path

load_dotenv()  # load environment variables from .env

CSV_FILE = "playback.csv"

# Volumio API
TOGGLE_PLAY_PAUSE_URL = "http://localhost:3000/api/v1/commands/?cmd=toggle"
STOP_URL = "http://localhost:3000/api/v1/commands/?cmd=stop"
PREVIOUS_URL = "http://localhost:3000/api/v1/commands/?cmd=prev"
NEXT_URL = "http://localhost:3000/api/v1/commands/?cmd=next"
GET_STATE_URL = "http://localhost:3000/api/v1/getState"
REPLACE_AND_PLAY_URL = "http://localhost:3000/api/v1/replaceAndPlay"

# Playback Control Tags
TOGGLE_PLAY_PAUSE_ID = os.getenv("TOGGLE_PLAY_PAUSE_ID")
STOP_ID = os.getenv("STOP_ID")
PREVIOUS_ID = os.getenv("PREVIOUS_ID")
NEXT_ID = os.getenv("NEXT_ID")

scanner = SimpleMFRC522()
last_id = None


def search(id):
    with open(CSV_FILE) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == id:
                return row["Service"], row["URI"], row["Name"]


def play(id):
    if search(id):
        service, uri, name = search(id)
        print(f"{name}\n")
        headers = {"content-type": "application/json"}
        payload = {"service": service, "uri": uri}
        requests.post(REPLACE_AND_PLAY_URL,
                      headers=headers, data=json.dumps(payload))
    else:
        print(f"The ID '{id}' could not be found in '{CSV_FILE}'.\n")


try:
    if Path(CSV_FILE).is_file():
        print("Ready to scan tag...\n")

        while True:
            id = str(scanner.read_id())
            if id:
                if id == last_id:
                    continue

                print(f"{id} ==> ", end="")

                if id == TOGGLE_PLAY_PAUSE_ID:
                    print("Play/Pause\n")
                    url = TOGGLE_PLAY_PAUSE_URL
                elif id == STOP_ID:
                    print("Stop\n")
                    url = STOP_URL
                elif id == PREVIOUS_ID:
                    print("Previous\n")
                    url = PREVIOUS_URL
                elif id == NEXT_ID:
                    print("Next\n")
                    url = NEXT_URL
                else:
                    last_id = id
                    play(id)

                try:
                    if url:
                        last_id = None
                        requests.get(url, timeout=0.1)
                        time.sleep(2.5)
                except:
                    pass

            else:
                if not last_id:
                    continue

                last_id = None
    else:
        print(f"The file '{CSV_FILE}' does not exist.\n")
        sys.exit()

finally:
    GPIO.cleanup()
