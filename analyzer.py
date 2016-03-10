#!/usr/bin/env python3

from collections import namedtuple
import csv
from datetime import datetime
import json


# First: get a dict of identifiers with their channel name
senderlist = {}
with open('senderlist.json') as fh:
    senderlist = json.load(fh, parse_int=str)
sender_identifiers = {}
for v in senderlist.values():
    sender_identifiers[v[0]] = v[1]


data = []
Slice = namedtuple('Slice', 'start end channelid')
with open('sniffed.csv', 'r') as fh:
    csvreader = csv.reader(fh)

    first = None  # begin of slice
    last = None  # end of slice
    channel = None  # channel id

    for row in csvreader:
        dt = datetime.fromtimestamp(float(row[0]))
        chan = row[1]

        # Initialize values
        if not first:
            first = dt
        if not channel:
            channel = chan
        if not last:
            last = dt

        if channel != chan:
            # Channel switched
            sl = Slice(first, last, channel)
            data.append(sl)

            first = dt
            last = dt
            channel = chan
            continue

        last = dt  # Update end of slice

    # Last entry
    sl = Slice(first, last, channel)
    data.append(sl)

timeformat = '%Y-%m-%d %H:%M.%S'
for e in data:
    print('From {} to {} channel {}'.format(
        e.start.strftime(timeformat),
        e.end.strftime(timeformat),
        sender_identifiers[e.channelid]
    ))
