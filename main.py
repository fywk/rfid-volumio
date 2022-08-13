#!/usr/bin/env python3

import csv
import os
import sys
import time
from pathlib import Path

import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from mfrc522 import SimpleMFRC522

load_dotenv()  # load environment variables from .env

# CSV file containing a list of tag IDs and and their corresponding playback URIs
CSV_FILE = "playback.csv"

# Volumio API endpoints
VOLUMIO_API_ROOT = "http://localhost:3000/api/v1"
TOGGLE_PLAY_PAUSE_URL = "commands/?cmd=toggle"
STOP_URL = "commands/?cmd=stop"
PREVIOUS_URL = "/commands/?cmd=prev"
NEXT_URL = "commands/?cmd=next"
REPLACE_AND_PLAY_URL = "replaceAndPlay"

# Tag IDs for playback controls
TOGGLE_PLAY_PAUSE_ID = os.getenv("TOGGLE_PLAY_PAUSE_ID")
STOP_ID = os.getenv("STOP_ID")
PREVIOUS_ID = os.getenv("PREVIOUS_ID")
NEXT_ID = os.getenv("NEXT_ID")

scanner = SimpleMFRC522()
last_id = None


def welcome():
    print("RFID Volumio - Control Volumio on Raspberry Pi via RFID")


def is_control_id(id, ids):
    return any(x == id for x in ids)


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
        payload = {"service": service, "uri": uri}
        requests.post(f"{VOLUMIO_API_ROOT}/{REPLACE_AND_PLAY_URL}", json=payload)
    else:
        print(f"The ID \"{id}\" could not be found in either '.env' or '{CSV_FILE}'.\n")


try:
    welcome()
    if Path(CSV_FILE).is_file():
        print("✔ Ready to scan...\n")
        while True:
            id = str(scanner.read_id())
            if id:
                if id == last_id:
                    continue

                print(f"{id} ==> ", end="")

                if is_control_id(
                    id, [TOGGLE_PLAY_PAUSE_ID, STOP_ID, PREVIOUS_ID, NEXT_ID]
                ):
                    if id == TOGGLE_PLAY_PAUSE_ID:
                        name = "Play/Pause"
                        url = TOGGLE_PLAY_PAUSE_URL
                    elif id == STOP_ID:
                        name = "Stop"
                        url = STOP_URL
                    elif id == PREVIOUS_ID:
                        name = "Previous"
                        url = PREVIOUS_URL
                    elif id == NEXT_ID:
                        name = "Next"
                        url = NEXT_URL

                    print(f"{name}\n")
                    last_id = None
                    requests.get(f"{VOLUMIO_API_ROOT}/{url}", timeout=0.1)
                    time.sleep(2.5)
                else:
                    last_id = id
                    play(id)
            else:
                if not last_id:
                    continue

                last_id = None
    else:
        print(f"✖ The file '{CSV_FILE}' does not exist.\n")
        sys.exit()

finally:
    GPIO.cleanup()
