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
# Minimal imports
from numpy import diff
from itertools import groupby
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
        # The following are initialized as placeholders to None or empty iterables. They will represent variables of the elevator's changing state
        self.next_floor = None
        self.floor_list = []
        self.floor_history = []
        self.floor_future = []
        
        assert self.start_height <= self.building_height, "The elevator may not start higher than the top floor."
    
    # Return None for now; essentially pass while developing
    @property
    def dist_to_next(self):
        if self.next_floor:
            return self.next_floor - self.current_height
        else:
            return None
    @property
    def time_to_next(self):
        if self.next_floor:
            return abs(self.dist_to_next) / self.speed
        else:
            return None
    @property
    def direction_to_next(self):
        if self.next_floor:
            if self.dist_to_next > 0:
                return "up"
            elif self.dist_to_next < 0:
                return "down"
            else:
                return "away"
        else: 
            return None
    @property
    def sum_dist_to_final(self):
        """Sum of the absolute differences between each current floor and the next to get the total distance traveled until the final floor.
        Returns: 
            int: Total integrated distance the elevator will take to get to the final floor in its list.
        """
        all_remaining_distances = diff([self.current_height]+self.floor_future)
        return sum(abs(all_remaining_distances))
    @property
    def sum_time_to_final(self):
        """Calculates the time it will take to go from the current position to the final floor.
        Returns:
            int: number of seconds to travel from the current floor to the final floor
        """
        return self.sum_dist_to_final / self.speed
    
    @property
    def report(self):
        """Generates a summary report of the elevator's state and future path.
        Returns:
            str: String representation of the summary report
        """
        report_string = "\n### REPORT ###\n" + f"{self.name} is currently on floor {self.current_height} of {self.building_name} with {self.building_height} floors." 
        # If it's not done moving through the inputs, add this section of text.
        if self.next_floor:
            report_string += f" The next floor ({self.next_floor}) is {abs(self.dist_to_next)} floors {self.direction_to_next} (ETA = {readable_time_delta(self.time_to_next)} seconds). The final commanded floor ({self.final_floor}) is {self.sum_dist_to_final} total floors away (ETA = {readable_time_delta(self.sum_time_to_final)} seconds)."
        return report_string
    
    def __repr__(self) -> str:
        return str(self.report)
    
    def travel_through_floor_list(self, floor_list, verbosity=2):
        # Remove subsequent duplicates in the floor_list; it's not meaningful to go from floor n to the same floor n.
        floor_list = [floor for floor, _group in groupby(floor_list)]
        # Set the floor_list to be the user-specified inputs list. 
        self.floor_list = floor_list
        # The floor_future begins as the same list, and has the visited floors removed from it.
        self.floor_future = self.floor_list
        # Check the floor list is allowed
        assert max(self.floor_list) <= self.building_height, "The elevator may never go higher than the top floor."
        # Set final floor
        self.final_floor = floor_list[-1]
        for floor in floor_list:
            self.next_floor = floor
            if verbosity > 1:
                print(self.report)
            # Keep track of where elevator is (current_height), has been (floor_history), and still needs to go (floor_future).
            self.current_height = floor
            self.floor_history.append(floor)
            self.floor_future = self.floor_future[1:]
        # At the end, set next_floor to None
        self.next_floor = None

#####
# Example instance for prototyping - remove before release!
e = Elevator(10,10, name="The Great Glass Elevator", building_name="The Chocolate Factory")
# print(e.report)
e.travel_through_floor_list([1,1,1,3,3,5])
print(e.report)

# %%
def readable_time_delta(num_seconds: int):
    """Converts integer number of seconds into a string which is more familiar/interpretable to humans. Only clarifies to the level of hours.
    Args:
        num_seconds (int): Number of seconds to convert into a string. Floats work as well, but suggested/type-hinted value is an integer, which works with expected number of seconds for integer floors and fractional speed.
    """
    if num_seconds < 60: # seconds range
        return str(num_seconds)
    elif num_seconds < 3600: # minutes range
        s_component = num_seconds % 60
        m_component = int(num_seconds / 60) # use int to round *down* to nearest int
        return f"{m_component} minutes {s_component} seconds"
    elif num_seconds < 24*3600: # hours range
        s_component = num_seconds % 60
        m_component = int((num_seconds % (3600)) / 60)
        h_component = int(num_seconds / 3600)
        return f"{h_component} hours {m_component} minutes {s_component:.1f} seconds"

# Example func call for prototyping - remove before release!
b = (3.5*(60**2))+43*60+12.3
readable_time_delta(b)
# %%