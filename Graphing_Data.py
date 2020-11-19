import pandas as pd
import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians

df = pd.read_csv('new_routes.csv')
af = pd.read_csv('airports.csv')

def getDistance(src, dest):
    R = 6371
    lat1, lon1 = src
    lat2, lon2 = dest

    dlat = radians(lat2-lat1)
    dlon = radians(lon2-lon1)
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return (R * c)

# Sort the paths based on distance from longest to shortest
# Generally the direct route will be the shortest path
def filterPaths(paths, src, dest):
    #L Loop through all paths 
    for path in paths:
        last = af.loc[af['IATA'] == src]
        lastC = (float(last.iloc[:, 6]), float(last.iloc[:, 7]))
        #print(path)
        distance = 0
        # Add the distance from each node to the last to get final distance
        for port in path[1:]:
            dinfo = af.loc[af['IATA'] == port]
            dcoord = (float(dinfo.iloc[:, 6]), float(dinfo.iloc[:, 7]))
            distance = getDistance(lastC, dcoord) + distance
            lastC = dcoord
        path.append(distance)
    # Sort the list based on the last element in each list
    paths.sort(key = lambda x: x[-1])
    print(paths)

def getAllAirportsInCountry(countries, ct):
    return countries.loc[countries['Country'] == ct] 

g = nx.Graph()
# Generate graph of nodes using networkX
for index, row in df.iterrows():
    g.add_edge(row[3], row[5], weight=row[10])

#graph = nx.from_pandas_edgelist(df, source='Source_Airport', target='Dest_Airport')

# Running
# while(True):
#     src = input('Source Aiport: ')
#     if src == 'close':
#         break
#     dest = input('Destination Aiport: ')
#     if dest == 'close':
#         break
#     lay = input('Max number of layovers: ')
#     lay = int(lay)+1
#     #depart = input('Departure Date: ')
#     #ret = input('Return Date: ')
#     paths = nx.all_simple_paths(g, source = src.upper(), target = dest.upper(), cutoff=int(lay))

#     #paths2 = nx.all_shortest_paths(g, source= src.upper(), target = dest.upper())
#     #filterPaths(list(paths), src.upper(), dest.upper())
#     for path in paths:
#         print(path)

a = getAllAirportsInCountry(af, "United Kingdom")
print(a)
