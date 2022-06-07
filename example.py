#!/usr/bin/env python3
"""
Title: example.py
Author: Nat Kerman (nathaniel.kerman@gmail.com)
Date (begun): 2022-06-06
Summary: File for showing examples of the Elevator class in the file elevator.py
"""
# %%
from elevator import Elevator, readable_time_delta
# Instantiates an Elevator
el = Elevator(X=0, Z=100, name="The Great Glass Elevator",
              building_name="The Chocolate Factory")
# Prints a report of the Elevator's state
print(el)
print("\n\n###### Now let's go for a ride! ######\n")
# Travel through a list of floors
el.travel_through_floor_list([1, 20, 3, 9, 100], verbosity=2)
# You can then send the same object to more floors
el.travel_through_floor_list([0, 11], verbosity=2)
# %%
# You can also read the history of the Elevator - where it's been, how long it's traveled in space and time, etc
print(f"The elevator named {el.name} has traveled {el.odometer} total floors in {readable_time_delta(el.time_elapsed)} seconds. Here's where it has been so far: {el.floor_history}.")
