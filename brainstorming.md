# Rough sketch of elevator concept for code test

Nat Kerman
2022-06-02

## Description of the task
As per email from Wendy Carande 2022-06-02:
(*key terms highlighted by Nat)*
>Construct a **class** that simulates an elevator that is on the **Xth floor of a Z story building**. The elevator travels at 1 floor/10 seconds (don't worry about acceleration/deceleration, etc.). **Input** will include a list of floor requests. **Output** will be: Current floor of the elevator, floors left to arrive at destination, time left to arrive at destination. Be sure to **list any assumptions** you feel should be known.
>The language preference is Python. Keep in mind we will want to run it, and we are interested in seeing software engineering best practices including documentation, readability, testing, etc.

## Key points extracted
1. "class" -> make it object oriented
2. speed of the elevator $\equiv v_{elevator} = \dfrac{1}{10}\dfrac{floors}{s}$
3. Floor of the elevator $\equiv X$ 
   1. Taking this to mean that X is the (constant) initial position of the elevator
   2. Floor of the elevator is same as saying the height in units of floors
4. Height of the building $\equiv Z$ (in floors)
   1. Also Z will be the maximum height of the elevator
   2. Test that height of the elevator $\equiv h$ never exceeds Z
      1. $h \le Z$
      2. It is *not* safe to assume that $h \ge 0$, because the building may have basement (negative) floors. Without more details, I will make the assumption that h may go as low as commanded by the inputs.
5. **Inputs:**
   1. List of floor requests
      1. e.g., `[1, 13, 83,...]`
   2. Inputs of the instance of the elevator class must be:
      1. initial height of elevator X (int)
      2. height of building Z (int)
6. **Outputs:**
   1. Current floor of the elevator (h)
   2. floors left to arrive at destination (distance_to_next)
   3. time left to arrive at destination (time_to_next)
      1. I'm assuming these should be returned by a function, but I'll also define some sort of verbosity function, and a \_\_repr\_\_ string.
         1. The \_\_repr\_\_ should look like: `f"Elevator {name} is currently on floor {h} of a building with {Z} floors. The next floor is {distance_to_next} floors away (ETA = {time_to_next} seconds). The final commanded floor is {distance_to_final} floors away (ETA = {time_to_final} seconds)."`

## Potential Strategy
1. Object Oriented Approach to the Elevator
   1. Central object is the elevator
   2. Properties:
      1. height of the building (Z)
         1. this could also be a global constant, but it's more versatile to make it a property of the elevator
      2. current floor (h)
      3. history - need to consider how best to hold this - consider tic-tac-toe example
      4. contents/weight/passengers (?) 
         1. not specified in the objectives - define a property and `pass` or set to None
2. Testing 
   1. Edgecases
      1. Empty list
      2. Repeats of same floor
      3. Non integer floors
         1. Both numerical types and strings/etc.
   2. Min/max floor
   3. Check expected times