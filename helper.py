import random
import numpy as np
import pandas as pd
import plotly.express as px
from matplotlib.pyplot import cm
import plotly.graph_objects as go

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
    depot_capacity = df_depots['Depot Capacity']
    depot_ids = df_depots['Depot ID']
    drop_ids = df_drops['Drop ID']
    return [depots, drops, depot_ids, drop_ids, depot_capacity]

def result_builder(allocation_list, depot_locations, drop_locations, depot_ids, drop_ids, depot_capacity):
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
            "depot_capacity": depot_capacity[depot_index]
        }
    return result

def plot_allocation_result_matplot(ax, allocation_result):
    color = cm.Dark2(np.linspace(0, 1, 100))

    x_depot = [] 
    y_depot = []
    depot_ids = []
    x_drop = []
    y_drop = []
    drop_ids = []

    for depot_id, depot_info in allocation_result.items():
        c = random.choice(color)
        depot_location = depot_info["depot_location"]
        drops = depot_info["drops"]
        x_depot.append(depot_location[0])
        y_depot.append(depot_location[1])
        depot_ids.append(depot_id)

        if len(drops) > 0:
            for drop_id, drop_info in drops:
                drop_location = drop_info["drop_location"]
                x_drop.append(drop_location[0])
                y_drop.append(drop_location[1])
                drop_ids.append(drop_id)
                ax.plot([depot_location[0], drop_location[0]], [depot_location[1], drop_location[1]], c = c, alpha=0.7, zorder=1)
    
    ax.scatter(x=x_depot, y=y_depot, color='r', s=100, zorder=2, label='Service Centers')
    ax.scatter(x=x_drop, y=y_drop, color='b', zorder=0, alpha = 0.7, label='Drops')
    
    return ax

def plot_allocation_result_plotly(allocation_result):
    x_depot = [] 
    y_depot = []
    depot_ids = []
    x_drop = []
    y_drop = []
    drop_ids = []
    color = px.colors.sequential.Inferno
    fig = go.Figure()

    for depot_id, depot_info in allocation_result.items():
        connector_color = random.choice(color)
        depot_location = depot_info["depot_location"]
        drops = depot_info["drops"]
        x_depot.append(depot_location[0])
        y_depot.append(depot_location[1])
        depot_ids.append(depot_id)

        if len(drops) > 0:
            for drop_id, drop_info in drops.items():
                drop_location = drop_info["drop_location"]
                x_drop.append(drop_location[0])
                y_drop.append(drop_location[1])
                drop_ids.append(drop_id)
                fig.add_trace(go.Scatter(x=[depot_location[0], drop_location[0]], y=[depot_location[1], drop_location[1]],
                    mode='lines+markers', showlegend=False, line_color=connector_color, hoverinfo="skip"))


    fig.add_trace(go.Scatter(x=x_drop, y=y_drop,
                    mode='markers',
                    name='Drops', hovertext=drop_ids, 
                    marker=dict(color='#848ff0', size=6, 
                    line=dict(width=1,color='DarkSlateGrey'))))
    fig.add_trace(go.Scatter(x=x_depot, y=y_depot,
                    mode='markers',
                    name='Depots', hovertext=depot_ids, 
                    marker=dict(color='red', size=12, 
                    line=dict(width=1,color='DarkSlateGrey'))))
    fig.update_layout(
        width=700,
        height=500,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        title={
        'text': "Package Allocation",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },
        xaxis_title="Latitude",
        yaxis_title="Longitude",
        paper_bgcolor="#D3D3D3",
        plot_bgcolor="#C0C0C0",
        font=dict(
            family="monospace",
            size=18,
            color="black"
        )
    )
    return fig
