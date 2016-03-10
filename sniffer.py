#!/usr/bin/env python2

"""IPTV-sniffer
If you have an IPTV provider and share the network with your receiver devices
chances are your network gets flooded with multicast UDP packages.

This tool is for demonstation purposes to show people how easy it is to
capture what they watch on television.
"""
import csv
from datetime import datetime
import json
import os
from time import sleep
from scapy.all import sniff, IP

# You need senderlist.txt and the parser to load the senderlist json
senderlist = {}
if os.path.exists('senderlist.json'):
    with open('senderlist.json', 'r') as fh:
        senderlist = json.load(fh)

collected_data = []  # (Datetime, [..Destinations..]) tuples

while True:
    try:
        now = datetime.now()
        timestamp_text = now.strftime('%Y-%m-%d %H:%M.%S')

        # Take snapshot with max 10 packets of udp traffic on port 10000
        # Times out after 1 second (if there are no packets)
        stats = sniff(iface='wire0', filter='udp and port 10000',
            count=10, store=True, timeout=1)

        # If no packets were logged, skip
        if len(stats) == 0:
            print('No packets captured at {}'.format(timestamp_text))
            continue

        targets = []  # Multiple iptv devices may use the same network
        for packet in stats:
            dest = packet[IP].dst
            if dest not in targets:
                sender = 'unknown'
                if dest in senderlist:
                    sender = senderlist[dest][1]

                print('{}: {}'.format(timestamp_text, sender))
                targets.append(dest)

        collected_data.append((now, targets))

        # Append to csv file
        with open('sniffed.csv', 'a') as fh:
            csvwriter = csv.writer(fh)
            for target in targets:  # if multiple channels at the same time
                identifier = 0
                if target in senderlist:
                    identifier = senderlist[target][0]
                csvwriter.writerow([now.strftime('%s'), identifier])

        # Sleep for a period of time.
        # When capturing with '10 packets and 1 second timeout' it logs multiple
        # times per second. If the capture has no packet limit but a timeout,
        # the 'stats' set grows really big.
        # So 'sleep' seems to be the most ressource friendly solution.
        sleep(5)
    except KeyboardInterrupt:
        # KeyboardInterrupt was needed before 'sleep' was introduced because
        # the 'while True' loop did not recognize single keyboard commands
        print(collected_data)
        break

