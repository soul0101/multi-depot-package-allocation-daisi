import random
import helper
import pandas as pd
import optimization
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import plotly.graph_objects as go

@st.cache(suppress_st_warning=True)
def allocate_packages(depot_locations, drop_locations, depot_ids=None, drop_ids=None, depot_capacities=None):
    """
    Runs the MIP solver 

    Parameters
    ----------
    depot_locations: 
        A list of tuples containing the (latitude, longitude) of each depot.
    drop_locations: 
        A list of tuples containing the (latitude, longitude) of each drop location.
    depot_ids: 
        A list of integers containing the id of each depot.
    drop_ids: 
        A list of integers containing the id of each drop location.
    depot_capacities: 
        A list of integers representing the maximum number of packages that can be allocated to each depot.

    Returns
    -------
    Dict containing the allocation information for each depot:
        {
            <depot_id> : {
                "depot_location": <array(latitude, longitude)>,
                "drops" : {
                            <drop_id1> : "drop_location": <array(latitude, longitude)>,
                            <drop_id2> : "drop_location": <array(latitude, longitude)>,
                        }
                "depot_capacity": int>
            }, ...
        }
    """

    depot_ids, drop_ids, depot_capacities = helper.sanitize(depot_ids, drop_ids, depot_capacities, len(depot_locations), len(drop_locations))
        
    allocation_list = optimization.optimize(depot_locations, drop_locations, depot_capacities)
    result = helper.result_builder(allocation_list, depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities)
    return result

def get_allocations_plot_plotly(allocation_result):
    """
    Returns a Plotly Figure
    """

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

################################## UI ##############################################

def st_ui():
    st.write("# Welcome to the Multi-Depot Package Allocation Daisi! 👋")
    st.markdown(
        """
            Consider a scenario of last mile delivery where packages are to be delivered to certain __drop__ locations. \n
            Each package first has to be sent to a __depot__ which handles its delivery to the final destination. \n
            Each __depot__ has a fixed __capacity__ and can only handle that many drops. \n
            Our task is to assign each drop to a depot and minimise the cost of delivery. \n
        """
    )
    

    col1, col2 = st.columns([1,1])

    with col1:
        st.header('Depots Data')
        df_depots = pd.read_csv('./data/city_depots1.csv')
        st.dataframe(df_depots)
    with col2:
        st.header('Drops Data')
        df_drops = pd.read_csv('./data/city_drops1.csv')
        st.dataframe(df_drops)

    [depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities] = helper.read_data()
    generate = st.button("Allocate Drops")
    if generate:
        with st.spinner("Calculating..."):
            result = allocate_packages(depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities)
            fig = get_allocations_plot_plotly(result)
            st.plotly_chart(fig, use_container_width=True)
            st.header("Result")
            st.json(result, expanded=False)

if __name__ == '__main__':
    st_ui()