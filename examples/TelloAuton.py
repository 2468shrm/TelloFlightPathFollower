
import time
from telloflightpathfollower import TelloFlightPathFollower
#
# A list of command dictionaries, each dictionary describing one step of the
# flight path
#
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

test_flight_2_list = [
    { 'cmd': 'takeoff', 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'counter_clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'counter_clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'land' },
]

test_flight_3_list = [
    { 'cmd': 'takeoff', 'delay_after': 2 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 25 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 25 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 50 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 50 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 50 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 25 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90 },
    { 'cmd': 'move', 'direction': 'forward', 'value': 25 },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 90, 'delay_after': 2 },
    { 'cmd': 'land' },
]

mission_2465_list = [
    { 'cmd': 'takeoff' },
    { 'cmd': 'report_padid' },
    { 'cmd': 'rotate', 'direction': 'clockwise', 'value': 38},
    { 'cmd': 'find', 'direction': 'forward', 'value': 40, 'padid': 2},
    { 'cmd': 'report_padid' },
    { 'cmd': 'land' },
]

flight_follower = TelloFlightPathFollower(debug=True)

tello_state_dict = flight_follower.tello.get_current_state()
print(f'tello state is: {tello_state_dict}')

flight_follower.set_flight_path(flight_path=test_flight_3_list)
flight_follower.run()
