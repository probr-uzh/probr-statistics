from pymongo import MongoClient
from bson.code import Code
import numpy as np
import matplotlib.pyplot as plt

client = MongoClient()

db = client['probr-core']

packets = []

for p in db.packets.find():
    packets.append(p['signal_strength'])

