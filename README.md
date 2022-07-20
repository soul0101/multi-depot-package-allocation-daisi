# multi-depot-package-allocation-daisi
Last mile delivery refers to the last leg of supply chain operations. A product's journey from a warehouse to the doorstep of the end-customer. This last step of the delivery process is most critical and should be optimized for a better user experience and dramatic reduction in operating costs.<br/>
This is a <b>Mixed Integer Programming (MIP)</b> model for allocating shipments to the nearest service centers while keeping in mind the capacity constraints.

## Test API Call
```python
import pydaisi as pyd
multi_depot_package_allocation = pyd.Daisi("soul0101/Multi-Depot Package Allocation")
"""
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
depot_capacity: 
    A list of integers representing the maximum number of packages that can be allocated to each depot.
"""
result = multi_depot_package_allocation.allocate_packages(depot_locations, drop_locations, depot_ids, drop_ids, depot_capacity).value
```
## Reference
https://github.com/soul0101/Multi-Depot-Package-Allocation