#!/usr/bin/env python3

import csv

number = input("Enter ID to find: ")

csv_file = csv.DictReader(open("../playback.csv", mode="r"))


def search(number):
    for row in csv_file:
        if row["ID"] == number:
            return row["Service"], row["URI"]


if search(number):
    uri, service = search(number)
    print(service)
    print(uri)
