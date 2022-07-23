import helper
import pandas as pd
import optimization
import streamlit as st

@st.cache(suppress_st_warning=True)
def allocate_packages(depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities):
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
    allocation_list = optimization.optimize(depot_locations, drop_locations, depot_capacities)
    result = helper.result_builder(allocation_list, depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities)
    return result


def get_allocations_plot_matplot(allocation_result):
    """
    Returns a Matplotlib Figure
    """
    return helper.plot_allocation_result_matplot(allocation_result)

def get_allocations_plot_plotly(allocation_result):
    """
    Returns a Plotly Figure
    """
    return helper.plot_allocation_result_plotly(allocation_result)

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
            fig = helper.plot_allocation_result_plotly(result)
            st.plotly_chart(fig, use_container_width=True)
            st.header("Result")
            st.json(result, expanded=False)

if __name__ == '__main__':
    st_ui()