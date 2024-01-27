#!/usr/bin/env python3

import evdev
import json

from evdev import ecodes, categorize, AbsInfo

devices_json = json.loads(input())
devices = []

for device_json in devices_json:
	capabilities = {}
	for etype, caps in device_json['capabilities'].items():
		etype = int(etype)

		if etype is ecodes.EV_KEY:
			capabilities[etype] = caps
		elif etype is ecodes.EV_REL:
			rels = []
			for cap in caps:
				rels.append((cap[0], evdev.AbsInfo(**cap[1])))
			capabilities[etype] = rels
		elif etype is ecodes.EV_ABS:
			abses = []
			for cap in caps:
				if cap[1]['min'] > cap[1]['max']:
					cap[1]['min'], cap[1]['max'] = cap[1]['max'], cap[1]['min']
				abses.append((cap[0], evdev.AbsInfo(**cap[1])))
			capabilities[etype] = abses
		else:
			raise ValueError("unexpected cap etype: %s" % (etype))

	device = evdev.UInput(capabilities, name=device_json['name'], vendor=device_json['vendor'], product=device_json['product'])
	devices.append(device)

print('Device created')

while True:
	event = json.loads(input())
	devices[event[0]].write(event[1], event[2], event[3])

# vim: noexpandtab ts=4 sw=4

