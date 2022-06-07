#!/usr/bin/env python3
"""
Title: test_elevator.py
Author: Nat Kerman (nathaniel.kerman@gmail.com)
Date (begun): 2022-06-05
Summary: File for testing the Elevator class and associated functions and methods in the file elevator.py
"""
# %%
from elevator import check_all_ints, readable_time_delta, Elevator
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
    with pytest.raises(AssertionError):
        # Fails if we send the elevator to a non-integer floor
        el = Elevator(0,10)
        el.travel_through_floor_list(["5.0",5.1])
    
# %%
def test_dist_traveled_and_repeat_floors():
    """Tests both whether the odometer keeps track of the distance traveled, and whether the class sucessfully ignores repeated subsequent floors.
    For the duplicated subsequent floors test, we check whether it's handled successfully both for first commanded floor == the starting floor, and for repeated subsequent values in the floor_lists.
    """
    el = Elevator(9,10)
    el.travel_through_floor_list([9,3,9,9,10], verbosity=0) 
    el.travel_through_floor_list([10,1,2,10,4], verbosity=0) 
    assert el.floor_history == [9,3,9,10,1,2,10,4], f"Floor history is unexpected: {el.floor_history}"
    assert el.odometer == 37, f"Odometer (distance traveled) is unexpected: {el.odometer}"
    # Second example test of the above
    el2 = Elevator(0,100)
    el2.travel_through_floor_list([1], verbosity=0) 
    el2.travel_through_floor_list([0], verbosity=0) 
    assert el2.floor_history == [0,1,0], f"Floor history is unexpected: {el.floor_history}"
    assert el2.odometer == 2, f"Odometer (distance traveled) is unexpected: {el.odometer}"
# %%
def test_time_elapsed():
    """Tests that the time elapsed in travel is as expected.
    """
    el = Elevator(0,100)
    assert el.time_elapsed == 0, "Initial time elapsed should be 0"
    el.travel_through_floor_list([1,11,1], verbosity=0)
    el.time_elapsed == 21 * 10, "After traveling 21 floors at 0.1 floor/sec, 210 sec should have elapsed."
    el.travel_through_floor_list([0,5,4,33], verbosity=0)
    el.time_elapsed == 57 * 10, "After traveling 21 then an additional 36 floors at 0.1 floor/sec, 570 sec should have elapsed."
# %%
def test_negative_floors():
    """Tests the behavior still works with negative floors.
    """
    el = Elevator(0,100)
    el.travel_through_floor_list([-100, 100, -1000], verbosity=0)
    assert el.floor_history == [0,-100,100,-1000], "History not correctly recorded for negative floors."
    assert el.odometer == 1400, "Distance traveled not correctly recorded for negative floors."
    assert el.time_elapsed == 1400*10, "Time elapsed in transit not correctly recorded for negative floors."
# %%
def test_check_all_ints():
    """Tests the function which checks all items in an iterable are ints.
    """
    with pytest.raises(AssertionError):
        # Fails if we give it non-int floors
        assert check_all_ints([1,3,3.1]), "Should fail to find only integers."
    # Succeeds if we give it only int-convertable floors
    assert check_all_ints([1,3,3.0,]), "Should succeed to find only integers, even when 3.0 is technically a float"
# %%
def test_non_integer_floors():
    """Tests that in an Elevator object, non-integer floors fail
    """
    with pytest.raises(AssertionError):
        # Fails if we try to give an Elevator non-int floors
        el = Elevator(11,10)
        el.travel_through_floor_list([1,3,3.1])
