#!/usr/bin/env python
"""
Title: elevator.py
Author: Nat Kerman (nathaniel.kerman@gmail.com)
Date (begun): 2022-06-05
Summary: A object-based representation of an elevator in a building of a given height. Built for a code test.
###
Assumptions:
Integer number of floors only.
The elevator cannot go higher than the maximum floor of the building (Z) but it can go lower than 0 (i.e. basement levels are negative, ground floor is zero.)

"""
# %%
class Elevator:
    """An object to simulate an elevator starting on floor X and moving through a building of height Z.
    Args: 
        X (int): Floor on which the elevator starts.
        Z (int): Height of the building in floors. Maximum height of the elevator.
    """
    def __init__(self, X: int, Z: int, speed: float=0.1, name: str="Elevator", building_name: str="a building") -> None:
        self.start_height = X
        self.current_height = self.start_height
        self.building_height = Z
        self.speed = speed
        self.name = name
        self.building_name = building_name
    
    # Return None for now; essentially pass while developing
    @property
    def dist_to_next(self):
        return None
    @property
    def time_to_next(self):
        return None
    @property
    def sum_dist_to_final(self):
        return None
    @property
    def sum_time_to_final(self):
        return None
    
    @property
    def report(self):
        report_string = f"{self.name} is currently on floor {self.current_height} of {self.building_name} with {self.building_height} floors. The next floor is {self.dist_to_next} floors away (ETA = {self.time_to_next} seconds). The final commanded floor is {self.sum_dist_to_final} floors away (ETA = {self.sum_time_to_final} seconds)."
        return report_string
    
    def __repr__(self) -> str:
        return str(self.report)
    
    def travel_through_floor_list(floor_list, verbosity=1):
        pass

#####
# Example instance for prototyping - remove before release!
Elevator(10,3, name="The Great Glass Elevator")
# %%