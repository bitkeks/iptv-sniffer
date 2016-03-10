#!/usr/bin/env python3

from configparser import SafeConfigParser
import json
import re

p = SafeConfigParser()
p.read('senderlist.txt')

pl = p['playlist']
sender_dict = {}

for key in pl:
    if key.startswith('file'):
        no = key[4:]
        address = pl[key]
        sender = pl['Title'+no]

        m = re.match('\(\d*\) (.*)', sender)
        sender = m.group(1)

        m = re.match('rtp://@([0-9\.]*):10000', address)
        address = m.group(1)

        sender_dict[address] = sender

with open('senderlist.json', 'w') as fh:
    json.dump(sender_dict, fh)
