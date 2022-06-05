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
        self.next_floor = None
        self.floor_list = []
        
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
        return None
    @property
    def sum_time_to_final(self):
        return None
    
    @property
    def report(self):
        """Generates a summary report of the elevator's state and future path.
        Returns:
            str: String representation of the summary report
        """
        report_string = "\n### REPORT ###\n" + f"{self.name} is currently on floor {self.current_height} of {self.building_name} with {self.building_height} floors." 
        
        if self.next_floor:
            report_string += f" The next floor ({self.next_floor}) is {abs(self.dist_to_next)} floors {self.direction_to_next} (ETA = {self.time_to_next} seconds). The final commanded floor is {self.sum_dist_to_final} floors away (ETA = {self.sum_time_to_final} seconds)."
        return report_string
    
    def __repr__(self) -> str:
        return str(self.report)
    
    def travel_through_floor_list(self, floor_list, verbosity=2):
        # Set the floor_list to be the user-specified inputs list
        self.floor_list = floor_list
        # Check the floor list is allowed
        assert max(self.floor_list) <= self.building_height, "The elevator may never go higher than the top floor."
        
        self.final_floor = floor_list[-1]
        for floor in floor_list:
            self.next_floor = floor
            if verbosity > 1:
                print(self.report)
            self.current_height = floor
                
        # At the end set next_floor to None
        self.next_floor = None

#####
# Example instance for prototyping - remove before release!
e = Elevator(10,10, name="The Great Glass Elevator")
# print(e.report)
e.travel_through_floor_list([1,2,3])
print(e.report)

# %%
