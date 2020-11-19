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

def getAllAirportsInCountry(airports, ct):
    return airports.loc[airports['Country'] == ct]


def topKCountries(airports, k):
    return airports['Country'].value_counts()[:k]

def boundedReachability(paths):
    reach = []
    for path in paths:
            if path not in reach:
                reach.append(path)
    reach.sort()
    return reach

g = nx.Graph()
# Generate graph of nodes using networkX
for index, row in df.iterrows():
    g.add_edge(row[3], row[5], weight=row[10])

#graph = nx.from_pandas_edgelist(df, source='Source_Airport', target='Dest_Airport')

# Running
while(True):
    test = input('What would you like to find out:\n1)Destination Information \n2)Trip Routes\n')
    # Destination Information Choices
    if test == '1':
        print('Destination Information')
        infochoice = input('What would you like to do:\n1)Country Airport Information \n2)Country with the most Airports\n3)Top K Countries with Airports\n')
        if infochoice == '1':
            country = input('Country: ')
            countryAirports = getAllAirportsInCountry(af, country)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(countryAirports['Name'])
        if infochoice == '2':
            print('Country with the most airports:\n', topKCountries(af, 1))
        if infochoice == '3':
            k = input('How many countries would you like to see: ')
            print('Top countries:\n', topKCountries(af, int(k)))
    
    #Route Information
    if test == '2':
        travelchoice = input("What would you like to do:\n1)Route from Point A to B\n2)Reachability of Airport\n")
        if travelchoice == '1':
            src = input('Source Aiport: ')
            if src == 'close':
                break
            dest = input('Destination Aiport: ')
            if dest == 'close':
                break
            lay = input('Max number of layovers: ')
            lay = int(lay)+1
            #depart = input('Departure Date: ')
            #ret = input('Return Date: ')
            paths = nx.all_simple_paths(g, source = src.upper(), target = dest.upper(), cutoff=int(lay))
            for path in paths:
                print(path)
        if travelchoice == '2':
            src = input('Source Aiport: ')
            cut = input('Max number of hops: ')
            cut = int(cut)+1
            paths = nx.single_source_shortest_path(g, source = src.upper(), cutoff = int(cut))
            print(boundedReachability(list(paths.keys())))
    print('\n')

#a = getAllAirportsInCountry(af, "United Kingdom")
#print(a)
