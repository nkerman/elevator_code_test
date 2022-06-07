#!/usr/bin/env python3
"""
Title: elevator.py
Author: Nat Kerman (nathaniel.kerman@gmail.com)
Date (begun): 2022-06-05
Summary: A object-based representation of an elevator in a building of a given height. Built for a code test.
###
Assumptions listed in README.md
"""
# %%
# Minimal imports
from numpy import diff
from itertools import groupby
# %%
def readable_time_delta(num_seconds: int):
    """Converts integer number of seconds into a string which is more familiar/interpretable to humans. Only clarifies to the level of hours. If time is negative, just returns negative number of seconds (as str). A helper function which does not make sense to be a method of the Elevator class.
    Args:
        num_seconds (int): Number of seconds to convert into a string. Floats work as well, but suggested/type-hinted value is an integer, which works with expected number of seconds for integer floors and fractional speed.
    """
    if num_seconds < 60: # seconds range
        return f"{num_seconds:.1f} seconds"
    elif num_seconds < 3600: # minutes range
        s_component = num_seconds % 60
        m_component = int(num_seconds / 60) # use int to round *down* to nearest int
        return f"{m_component} minutes {s_component:.1f} seconds"
    else: # hours and longer range
        s_component = num_seconds % 60
        m_component = int((num_seconds % (3600)) / 60)
        h_component = int(num_seconds / 3600)
        return f"{h_component} hours {m_component} minutes {s_component:.1f} seconds"
# %%
def check_all_ints(iterable: list):
    """Check whether all the values in an iterable are equivalent to integers. Note that the float 5.0 is allowed, as well as the int 5.
    Args:
        iterable (list): List of items. 
    Returns:
        Bool: Whether all values are equivalent to integers.
    """
    # NOTE: Opted against using list comprehension for readability with multiple if statements
    all_bools = []
    for item in iterable:
        if isinstance(item, int):
            all_bools.append(True)
        elif isinstance(item, float):
            # 5.0 is allowed as it's equivalent to an integer
            all_bools.append(item.is_integer())
        else:
            all_bools.append(False)
    # Return True only if all of the values are equivalent to an int.
    return all(all_bools)
# %%
class Elevator:
    """An object to simulate an elevator starting on floor X and moving through a building of height Z.
    """
    def __init__(self, X: int, Z: int, speed: float=0.1, name: str="Elevator", building_name: str="a building") -> None:
        """Function to instantiate the Elevator object.

        Args:
            X (int): Floor on which the elevator starts.
            Z (int): Height of the building in floors. Maximum height of the elevator.
            speed (float, optional): How fast the elevator moves, in floors/second. Defaults to 0.1.
            name (str, optional): Name for the elevator. Defaults to "Elevator".
            building_name (str, optional): Name for the building. Defaults to "a building".
        """
        self.start_floor = X
        self.current_floor = self.start_floor
        self.building_height = Z
        self.speed = speed
        self.name = name
        self.building_name = building_name
        # The following are initialized as placeholders to None or empty iterables. They will represent variables of the elevator's changing state
        self.next_floor = None
        self.floor_list = []
        self.floor_history = []
        self.floor_future = []
        self.odometer = 0 # keeps track of distance traveled 
        self.time_elapsed = 0 # keeps track of time spent traveling 
        # Add the starting position to the floor_history
        self.floor_history.append(self.current_floor)
        # Make sure the Elevator doesn't start higher than the building allows.
        assert self.start_floor <= self.building_height, "The elevator may not start higher than the top floor."
    
    @property
    def dist_to_next(self):
        """Find distance to the next floor.
        Returns:
            int: Distance (signed numerical) to the next floor, in number of floors. None if no next floor is set.
        """
        if self.next_floor:
            return self.next_floor - self.current_floor
        else:
            return None
    @property
    def time_to_next(self):
        """Find the time it will take to arrive at the next floor, in seconds.
        Returns:
            int: Time (numerical) to arrive at next floor. None if no next floor is set.
        """
        if self.next_floor:
            return abs(self.dist_to_next) / self.speed
        else:
            return None
    @property
    def direction_to_next(self):
        """Determines if the next floor is up, down or the same floor, and returns the best word for the report
        Returns:
            str: word to use in the report - i.e. 'up' in the phrase '...10 floors up...'
        """
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
        all_remaining_distances = diff([self.current_floor]+self.floor_future)
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
        report_string = "\n### REPORT ###\n" + f"{self.name} is currently on floor {self.current_floor} of {self.building_name} with {self.building_height} floors." 
        # If it's not done moving through the inputs, add this section of text.
        if self.next_floor:
            report_string += f" The next floor ({self.next_floor}) is {abs(self.dist_to_next)} floors {self.direction_to_next} (ETA = {readable_time_delta(self.time_to_next)}). The final commanded floor ({self.final_floor}) is {self.sum_dist_to_final} total/integrated floors away (ETA = {readable_time_delta(self.sum_time_to_final)})."
        elif not self.next_floor:
            report_string += "\nThis is the final commanded floor."
        return report_string
    
    def __repr__(self) -> str:
        """Define a representation string for repr() function"""
        return str(self.report)
    
    def travel_through_floor_list(self, floor_list: list, verbosity: int=2):
        """Core method for iterating through a user-specified list of floors, and changing the state of the elevator to represent this motion. Optionally prints a report at each floor (verbosity=1), or only at the end of the elevator's motion (verbosity=1).

        Args:
            floor_list (list | tuple of int): The floors to go through. Must contain only integers; Non-integer floors are currently unsupported
            verbosity (int, optional): Whether to print a report at each floor (2+), just at the end of motion (1), or never (0). Defaults to 2.
        """
        # Make sure the input is iterable like a list or tuple. If a single value, convert it to a list containing that value
        if not isinstance(floor_list, (list, tuple)):
            floor_list = [floor_list]
        # Make sure the list isn't empty
        assert len(floor_list), "The input list must contain some floors."
        # Make sure the list contains only integer or integer-equivalent floats.
        assert check_all_ints(floor_list), "All values in the floor list must be ints or int-valued floats. "
        # Remove subsequent duplicates in the floor_list; it's not meaningful to go from floor n to the same floor n.
        floor_list = [floor for floor, _group in groupby(floor_list)]
        # If the first requested floor is the current floor, remove it from the list for similar reasons - it doesn't make sense to go from floor X to floor X.
        if floor_list[0] == self.current_floor:
            floor_list = floor_list[1:]
        # Now check there are still floors to visit:
        assert len(floor_list), "The input list must contain some floors which the elevator is not currently on."
        # Set the floor_list to be the cleaned, user-specified inputs list. 
        self.floor_list = floor_list
        # The floor_future begins as the same list, and has the visited floors removed from it.
        self.floor_future = self.floor_list
        # Check the floor list is allowed
        assert max(self.floor_list) <= self.building_height, "The elevator may never go higher than the top floor."
        # Set final floor
        self.final_floor = floor_list[-1]
        for floor in floor_list:
            self.next_floor = floor
            self.odometer += abs(self.next_floor - self.current_floor) # add distance traveled
            if self.next_floor:
                self.time_elapsed += self.time_to_next
            if verbosity > 1:
                print(self.report)
            # Keep track of where elevator is (current_floor), has been (floor_history), and still needs to go (floor_future).
            self.current_floor = floor
            self.floor_history.append(floor)
            self.floor_future = self.floor_future[1:]
        # At the end of the list, set next_floor to None
        self.next_floor = None
        if verbosity > 0:
            print(self.report)

# %%