#!/usr/bin/env python2

from datetime import datetime
import json
from scapy.all import sniff, IP

senderlist = None
with open('senderlist.json', 'r') as fh:
    senderlist = json.load(fh)

collected_data = []  # (Datetime, [..Destinations..]) tuples

for i in range(3):
    now = datetime.now()
    # Take 3 second snapshot of udp traffic on port 10000
    stats = sniff(iface='wire0', filter='udp and port 10000',
        count=None, store=True, timeout=3)

    if len(stats) == 0:
        print('No packets captured at {}'.format(now.strftime('%Y-%m-%d %H:%M.%S')))

    targets = []
    for packet in stats:
        dest = packet[IP].dst
        if dest not in targets:
            sender = 'unknown'
            if dest in senderlist:
                sender = senderlist[dest]

            print('{}: {}'.format(now.strftime('%Y-%m-%d %H:%M.%S'), sender))
            targets.append(dest)

    collected_data.append((now, targets))

print(collected_data)
