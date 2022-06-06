#!/usr/bin/env python
"""
Title: test_elevator.py
Author: Nat Kerman (nathaniel.kerman@gmail.com)
Date (begun): 2022-06-05
Summary: File for testing the Elevator class and associated methods in the file elevator.py
"""
# %%
from elevator import readable_time_delta, Elevator
import pytest
# %%
def test_readable_time_delta():
    # First a long, many day time string
    time_in_sec = (13*24*60*60) + (43*60*60) + (14*60) + 11.54
    assert readable_time_delta(time_in_sec) == "355 hours 14 minutes 11.5 seconds", "Incorrect time conversion"
    # Now for 0 time
    assert readable_time_delta(0) == "0.0 seconds", "Incorrect time conversion"
    # negative time
    assert readable_time_delta(-10000) == "-10000.0 seconds", "Incorrect time conversion"
# %%
def test_instantiate_Elevator():
    el = Elevator(10,11, name="The Great Glass Elevator", building_name="The Chocolate Factory")
    assert el.name == "The Great Glass Elevator", "Failed to instantiate"
    assert el.building_name == "The Chocolate Factory", "Failed to instantiate"
    assert el.building_height == 11, "Failed to instantiate"
    assert el.start_floor == 10, "Failed to instantiate"
    assert el.speed == 1/10, "Failed to instantiate"
    

# %%
def test_errors():
    """In certain circumstances, we want to generate errors if the user tries to specify an input outside of the system's limits.
    """
    with pytest.raises(AssertionError):
        # Fails if we start elevator higher than max floor of building
        Elevator(11,10)
    with pytest.raises(AssertionError):
        # Fails if we try to send the elevator higher than max floor of building
        el = Elevator(9,10)
        el.travel_through_floor_list([1,2,3,4,11,1,2,3,3])
    with pytest.raises(AssertionError):
        # Fails if we give the elevator an empty list
        el = Elevator(0,10)
        el.travel_through_floor_list([])
    with pytest.raises(AssertionError):
        # Fails if we give the elevator a list with only the current floor
        el = Elevator(0,10)
        el.travel_through_floor_list([0,0,0])
    
# %%
def test_dist_traveled_and_repeat_floors():
    """Tests both whether the odometer keeps track of the distance traveled, and whether the class sucessfully ignores repeated subsequent floors.
    For the duplicated subsequent floors test, we check whether it's handled successfully both for first commanded floor == the starting floor, and for repeated subsequent values in the floor_lists.
    """
    el = Elevator(9,10)
    el.travel_through_floor_list([9,3,9,9,10], verbosity=1) 
    el.travel_through_floor_list([10,1,2,10,4], verbosity=1) 
    assert el.floor_history == [9,3,9,10,1,2,10,4], f"Floor history is unexpected: {el.floor_history}"
    assert el.odometer == 37, f"Odometer (distance traveled) is unexpected: {el.odometer}"
    # Second example test of the above
    el2 = Elevator(0,100)
    el2.travel_through_floor_list([1], verbosity=0) 
    el2.travel_through_floor_list([0], verbosity=0) 
    assert el2.floor_history == [0,1,0], f"Floor history is unexpected: {el.floor_history}"
    assert el2.odometer == 2, f"Odometer (distance traveled) is unexpected: {el.odometer}"
# %%
