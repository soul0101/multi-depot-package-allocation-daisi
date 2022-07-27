import random

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

def sanitize(depot_ids, drop_ids, depot_capacities, num_depot, num_drop):
    if depot_ids is None:
        depot_ids = list(range(num_depot))
    if drop_ids is None:
        drop_ids = list(range(num_drop))
    if depot_capacities is None:
        depot_capacities = num_depot * [100]
    
    return depot_ids, drop_ids, depot_capacities

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
