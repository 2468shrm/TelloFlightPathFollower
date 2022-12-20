# TelloFlightPathFollower
This is a simple wrapper to the djitellopy object (for use with the EDU version of the
Tello drone).  This wrapper flys the drone using a sequence (list) of dict() objects that
describe the flight path.

## WARNING and Disclaimer
**This software is still in early development and has limited testing. Use at your own risk.
This could cause your drone to fall from the sky and damage itself.**

Especially the manual control portions of the code.

## Required python Modules
This object requires two modules be installed: djitellopy and pygame.
- djitellpy is used to interface with the drone and it uses the Tello object of this module.
- pygame is used for a keyboard interface and is used if the drone recieves a 'manual' command or the auto list is exhausted/consumed.

### Installation of Required Modules
We recommend you install things in a virtual environment and activate it prior to use.
```
$ python -m venv TelloENV
$ pip3 install djitellopy
$ pip3 install pygame
```

## Flight Path Description

The dicts() have a simple structure:

`{ 'cmd': command_str, option_str: option_str_value, ... }`

Where the command_str is one of:
- 'takeoff'
  - The drone takes off.
  - Example
    - ```{ 'cmd': 'takeoff' }```
- 'land'
  - The drone lands.
  - Example
    - ```{ 'cmd': 'land' }```
- 'report_padid'
  - This prints the current pad ID to the console (useful for debugging flight paths that search for pads).
  - Example
    - ```{ 'cmd': 'report_padid' }```

- 'rotate'
  - The drone rotates in a specified direction (based on the 'direction' key/value) a specific angle (based on the 'angle' key/value) in degrees.
  - Rotation examples:
    - ```{ 'cmd': 'rotate', 'direction': 'clockwise', 'angle': value }```
    - ```{ 'cmd': 'rotate', 'direction': 'counter_clockwise', 'angle': value }```

- 'move'
  - The drone moves in a specified direction (based on a 'direction' key/value) a distance (based on a 'value' key/value) in cm.
  - Movement examples:
    - ```{ 'cmd': 'move', 'direction': 'up', 'value': value }```
    - ```{ 'cmd': 'move', 'direction': 'down', 'value': value }```
    - ```{ 'cmd': 'move', 'direction': 'left', 'value': value }```
    - ```{ 'cmd': 'move', 'direction': 'right', 'value': value }```
    - ```{ 'cmd': 'move', 'direction': 'forward', 'value': value }```
    - ```{ 'cmd': 'move', 'direction': 'bac', 'value': value }```

- 'find'
  - The drone moves in a specified direction (based on a 'direction' key/value) a distance (based on a 'distance' key/value) in cm per step, looking for a specific pad ID (based on the 'padid' key/value).
  - Note that the find command is 'repeated', i.e. it moves a distance and looks for the pad ID and reoeats until it finds it.
  - Movement examples:
    - ```{  'cmd': 'find', 'direction': 'forward', 'distance': value, 'padid': value }```
    - ```{  'cmd': 'find', 'direction': 'back', 'distance': value, 'padid': value }```
    - ```{  'cmd': 'find', 'direction': 'left', 'distance': value, 'padid': value }```
    - ```{  'cmd': 'find', 'direction': 'right', 'distance': value, 'padid': value }```

- 'manual'
  - Switches the control of the drone to manual control via keyboard input.
  - Start/End
    - `T` Takeoff
    - `L` Land
  - Translate
    - &#8593; Forward
    - &#8595; Backward
    - &#8592; Left
    - &#8594; Right
  - Yaw
    - `A` Rotate counter clockwise
    - `D` Rotate clockwise (yaw)
  - Vertical
    - `W` Up
	- `S` Down

- There are a couple of key/value modifiers that apply to commands.
  - 'delay_before': delay_in_seconds. Delays the execution of the command by the value before execution.
  - 'delay_after': delay_in_seconds. After executing the current command, it delays the start of the next command by the value.
  - `step_speed`: speed in cm/s. Provides a temporary speed override to the current dict(). Useful for movement where increased speed does not result in autonomous variation. At the end of the execution of the dict(), it restores the default speed.

## A Flight Path Example (or two)

### Example 1 (Test Flight #1)
This path tests vertical and translation movements. This sequence has the drone fly in multiple directions at multiple altitudes.
```
test_flight_1_list = [
    { 'cmd': 'takeoff', },
    { 'cmd': 'move', 'direction': 'left', 'value': 30 },
    { 'cmd': 'move', 'direction': 'up', 'value': 40 },
    { 'cmd': 'move', 'direction': 'right', 'value': 30 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 30 },
    { 'cmd': 'move', 'direction': 'down', 'value': 40 },
    { 'cmd': 'move', 'direction': 'back', 'value': 30 },
    { 'cmd': 'land' },
]
```

### Example 2 (Test Flight #2)
THis path tests yaw movements.
```
test_flight_2_list = [
    { 'cmd': 'takeoff', 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'counter_clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'counter_clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'land' },
]
```

### Example 3
This example shows full use of the flight path follower object.

```
import time
from telloflightpathfollower import TelloFlightPathFollower

# This uses the flight path from the previous (#2) example
test_flight_2_list = [
    { 'cmd': 'takeoff', 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'counter_clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'counter_clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'land' },
]
flight_follower = TelloFlightPathFollower(debug=True)

tello_state_dict = flight_follower.tello.get_current_state()
print(f'tello state is: {tello_state_dict}')

flight_follower.set_flight_path(flight_path=test_flight_3_list)
flight_follower.run()
```
