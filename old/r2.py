#!/usr/bin/env python

from random import random

hist = {}
spincount = {
		'first': 0,
		'second': 0,
		'third': 0,
		'green': 0
	}

# list of max spincount values in each series during reset so we can avg later
spinseries = {
		'first': [],
		'second': [],
		'third': [],
		'green': []
}

total_count = 0
while total_count < 10000000:
	count = 0
	while count < 1000000:
		count += 1
		spin = int(random()*10000) % 38
		if spin in [0, 37]:
			# zero, double-zero
			dozen = 'green'
		elif spin < 13:
			dozen = 'first'
		elif spin < 25:
			dozen = 'second'
		else:
			dozen = 'third'
		
		spinseries[dozen] += [spincount[dozen]]

		for k in spincount:
			spincount[k] += 1

		spincount[dozen] = 0
			
	total_count += count
	print("\nAfter %d:" % total_count)

	for k in ['first', 'second', 'third', 'green']:
		print("%10s: (min/max/avg): %0.2f/%0.2f/%0.2f" % (k, min(spinseries[k]), max(spinseries[k]), (float(sum(spinseries[k]))/len(spinseries[k]))))


print("\nMedians")
for k in ['first', 'second', 'third', 'green']:
	print("%10s: %d" % (k, sorted(spinseries[k])[len(spinseries[k])/2]))

print("\n% over 10 spins:")
for k in ['first', 'second', 'third', 'green']:
	print("%10s: %0.2f" % (k, float(len([x for x in spinseries[k] if x > 10]))/len(spinseries[k])*100))

print("\nbreakdown:")
for k in ['first', 'second', 'third', 'green']:
	valcount = {}
	for series in spinseries[k]:
		if str(series) in valcount:
			valcount[str(series)] += 1
		else:
			valcount[str(series)] = 1
	
	print("\n\t%s" % k)
	for l in sorted(valcount.keys()):
		print("\t\t%5s: %d" % (l, valcount[l]))

