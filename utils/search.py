#!/usr/bin/env python3

import csv

number = raw_input("Enter ID to find: ")

csv_file = csv.DictReader(open("../playback.csv", mode="r"))


def search(number):
    for row in csv_file:
        if number == row["ID"]:
            return row["Service"], row["URI"]

uri, service = search(number)
print(service)
print(uri)