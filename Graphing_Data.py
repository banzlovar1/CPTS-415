import pandas as pd
import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians

df = pd.read_csv('new_routes.csv')
af = pd.read_csv('airports.csv')
airlines = pd.read_csv('airlines.csv')

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

def airlineAggregation():
    a = airlines.loc[airlines['Country'] == 'United States']
    return a.loc[a['Active']=='Y']

g = nx.Graph()
# Generate graph of nodes using networkX
for index, row in df.iterrows():
    if row[3] != row[5]:
        g.add_edge(row[3], row[5], weight=row[10])

#graph = nx.from_pandas_edgelist(df, source='Source_Airport', target='Dest_Airport')

# Running
while(True):
    test = input('What would you like to find out:\n1)Destination Information \n2)Trip Routes\n')
    # Destination Information Choices
    if test == '1':
        print('Destination Information')
        infochoice = input('What would you like to do:\n1)Country Airport Information \n2)Country with the most Airports\n3)Top K Countries with Airports\n4)Active Airlines in the US\n')
        # Country airport info
        if infochoice == '1':
            country = input('Country: ')
            countryAirports = getAllAirportsInCountry(af, country)
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(countryAirports['Name'])
        # Top Country
        if infochoice == '2':
            print('Country with the most airports:\n', topKCountries(af, 1))
        # Top K Countries
        if infochoice == '3':
            k = input('How many countries would you like to see: ')
            print('Top countries:\n', topKCountries(af, int(k)))
        # Airline Aggregation
        if infochoice == '4':
            activeAirlines = airlineAggregation()
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(activeAirlines['Name'])
    
    #Route Information
    if test == '2':
        travelchoice = input("What would you like to do:\n1)Route from Point A to B\n2)Reachability of Airport\n")
        # Reachability
        if travelchoice == '1':
            src = input('Source Aiport: ')
            if src == 'close':
                break
            dest = input('Destination Aiport: ')
            if dest == 'close':
                break
            lay = input('Max number of layovers: ')
            if lay == '':
                print(nx.shortest_path(g, source = src.upper(), target = dest.upper()))
            # Constrained Reachability
            else:
                l = int(lay)+1
                paths = nx.all_simple_paths(g, source = src.upper(), target = dest.upper(), cutoff=int(l))
                for path in paths:
                    print(path)
        # Single Source Bounded Reachability 
        if travelchoice == '2':
            src = input('Source Aiport: ')
            cut = input('Max number of hops: ')
            cut = int(cut)+1
            paths = nx.single_source_shortest_path(g, source = src.upper(), cutoff = int(cut))
            print(boundedReachability(list(paths.keys())))
    print('\n')
