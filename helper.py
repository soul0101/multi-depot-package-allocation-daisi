import random
import numpy as np
import pandas as pd

def generate_locs_two_region(num_rows):
    lat = [18.627160, 18.621160]
    lon = [73.810552, 73.860552]

    result = []

    for _ in range(num_rows):
        dec_lat = random.random()/100
        dec_lon = random.random()/100
        result.append((random.choice(lat) + dec_lat, random.choice(lon) + dec_lon))
    return result

def generate_locs(num_rows):
    lat = (18.627160 + 18.621160)/2
    lon = (73.810552 + 73.860552) / 2

    result = []

    for _ in range(num_rows):
        dec_lat = random.random()/100
        dec_lon = random.random()/100
        result.append((lat + dec_lat, lon + dec_lon))
    return result

def read_data():
    df_depots = pd.read_csv('./data/city_depots1.csv')
    df_drops = pd.read_csv('./data/city_drops1.csv')

    depots = np.column_stack((df_depots['Latitude'], df_depots['Longitude']))
    drops = np.column_stack((df_drops['Latitude'], df_drops['Longitude']))
    depot_capacities = df_depots['Depot Capacity']
    depot_ids = df_depots['Depot ID']
    drop_ids = df_drops['Drop ID']
    return [depots, drops, depot_ids, drop_ids, depot_capacities]

def result_builder(allocation_list, depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities):
    result = {}
    for depot_index, drop_list in allocation_list.items():
        drops_info = {}
        for drop_index in drop_list:
            drops_info[drop_ids[drop_index]] = {
                "drop_location": drop_locations[drop_index]
            }

        result[depot_ids[depot_index]] = {
            "depot_location": depot_locations[depot_index],
            "drops": drops_info,
            "depot_capacity": depot_capacities[depot_index]
        }
    return result

