from pymongo import MongoClient
from bson.code import Code
import numpy as np
import matplotlib.pyplot as pl


client = MongoClient()

db = client['probr-core']

map = Code("function () { emit(this.signal_strength,1); }")

reduce = Code("function (key, values) { var sum = 0; for(var i=0; i < values.length ; i++){sum += values[i];} return sum;}")

statistics_collection = db.packets.map_reduce(map, reduce, "statistics")


#simple bar chart showing distribution of signal strength

values = []
bins = []
for s in statistics_collection.find():
    values.append(s['value'])
    bins.append(s['_id'])

fig = pl.figure()
ax = pl.subplot(111)
ax.bar(bins, values)
pl.title("Distribution of signal strength")
pl.ylabel("Number of packets")
pl.xlabel("Signal Strength in dBm")
pl.savefig("signalstrength_barchart.png", format='png')
pl.clf()


#cumulative distribution function of signal strength

cumulative_values = []

last_val = 0;

for i in xrange(len(values)):
    if i != 0:
        values[i] = values[i] + values[i-1]


fig, ax1 = pl.subplots()

ax1.plot(bins, values, 'bo')
pl.title("Cumulative distribution of signal strength")
ax1.set_ylabel("number of packets")
ax1.set_xlabel("signal Strength in dBm")
ax2 = ax1.twinx()
ax2.set_ylabel("percent")
ax2.yaxis.grid(True, which='major')
ax2.set_yticks([0.1,0.3,0.5,0.7,0.9], minor=True)
ax2.yaxis.grid(True, which='minor')
pl.savefig("signalstrength_cumulative_dsitribution.png", format='png')
pl.clf()