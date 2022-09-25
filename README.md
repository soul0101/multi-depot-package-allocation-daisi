# Multi Depot Package Allocation Daisi - [Live App](https://app.daisi.io/daisies/soul0101/Multi-Depot%20Package%20Allocation/app)

<p align="center">
    <img src="https://user-images.githubusercontent.com/53980340/192162736-dd6b77da-22f6-40ee-907a-2c7b9366b91c.png" alt="Logo" width="700">        
</p>



Last mile delivery refers to the last leg of supply chain operations. A product's journey from a warehouse to the doorstep of the end-customer. This last step of the delivery process is most critical and should be optimized for a better user experience and dramatic reduction in operating costs.<br/>
This is a <b>Mixed Integer Programming (MIP)</b> model for allocating shipments to the nearest service centers while keeping in mind the capacity constraints.

## Test API Call

```python
import pydaisi as pyd

multi_depot_package_allocation = pyd.Daisi("soul0101/Multi-Depot Package Allocation")

# Get dummy data
depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities = multi_depot_package_allocation.get_dummy_data().value

# Generate results
res = multi_depot_package_allocation.allocate_packages(depot_locations, drop_locations, depot_ids, drop_ids, depot_capacities).value

# Plot results
fig = multi_depot_package_allocation.get_allocations_plot_plotly(res).value
fig.show()
```

## Reference

https://github.com/soul0101/Multi-Depot-Package-Allocation
