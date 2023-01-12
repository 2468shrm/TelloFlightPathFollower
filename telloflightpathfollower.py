
import time
from djitellopy import Tello
import pygame


class TelloFlightPathFollower:
    def __init__(self, tello=None, flight_path=None, default_speed=10,
                 debug=False):
        # Store the incoming parameters to the class isntance variables
        self.debug = debug
        self.default_speed = default_speed

        if self.debug:
            print(f'debug enabled')
            print(f'creating TelloFlightPathFollower object')

        # Either use the passed Tello object, or create one if not provided.
        if tello:
            if self.debug:
                print(f'using passed Tello object')
            self.tello = tello
        else:
            if self.debug:
                print(f'creating Tello object')
            self.tello = Tello()

        if not self.tello:
            print('could not create a Tello object')
            quit()

        # Connect
        if self.debug:
            print(f'connecting..')
        self.tello.connect()
        if self.debug:
            print(f'..connected')

        self.tello.set_speed(self.default_speed)

        if self.debug:
            print(f'initial battery power is {self.tello.get_battery()}')

        self.tello.enable_mission_pads()
        # Look down for mission pads (only down, not forward too)
        self.tello.set_mission_pad_detection_direction(0)

        if not flight_path:
            if self.debug:
                print(f'no flight path declared on object creation')
        else:
            if self.debug:
                print(f'flight path declared on object creation')
        self.flight_path = flight_path

        # used during the step() method to see if a step_speed override
        # has been used, if so, restore speed at end of step...
        self.step_speed_override = False

        # The remainder of this class deals with manual (keyboard) control of
        # the drone.
        # Init pygame for eventual manual control
        pygame.init()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False
        # Speed of the drone
        self.S = 60

        # Update rate
        self.FPS = 120

    def manual_control_init(self):
        self.update_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.update_event, 1000 // self.FPS)
        print('The controls are:')
        print(' - T: Takeoff')
        print(' - L: Land')
        print(' - Arrow keys: Forward, backward, left and right.')
        print(' - A and D: Counter clockwise and clockwise rotations (yaw)')
        print(' - W and S: Up and down.)')

    def manual_control_run(self, do_connect=False):
        should_stop = False
        while not should_stop:
            for event in pygame.event.get():
                if event.type == self.update_event:
                    self.manual_control_update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.tello.is_flying:
                            if self.debug:
                                print('WARNING: Escaping while flying'
                                      ' results in a crash')
                                print('WARNING: Initiating auto land first!')
                            self._land()
                        should_stop = True
                    else:
                        self.manual_control_keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.manual_control_keyup(event.key)

            time.sleep(1/self.FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    def manual_control_keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = self.S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -self.S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -self.S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = self.S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = self.S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -self.S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -self.S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = self.S

    def manual_control_keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:
            # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:
            # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:
            # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:
            # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False

    def manual_control_update(self):
        """ Update routine. Send velocities to Tello.
        """
        if self.send_rc_control:
            """
            self.tello.send_rc_control(self.left_right_velocity,
                self.for_back_velocity, self.up_down_velocity,
                self.yaw_velocity)
            """
            print(f'{self.left_right_velocity}, {self.for_back_velocity},'
                  f'{self.up_down_velocity}, {self.yaw_velocity}')

    def set_flight_path(self, flight_path):
        if self.debug:
            print(f'setting flight_path')
        self.flight_path = flight_path

    #
    # Functions for vertical changes (take off, land, move up)
    #
    def _takeoff(self):
        if self.debug:
            print(f'taking off')
        self.tello.takeoff()

    def _land(self):
        if self.debug:
            print(f'landing')
        self.tello.land()

    def _move_up(self, x):
        if self.debug:
            print(f'moving up by {x}')
        self.tello.move_up(x)

    def _move_down(self, x):
        if self.debug:
            print(f'moving down by {x}')
        self.tello.move_down(x)

    #
    # Functions for translational (parallel to ground) movement (forward, back,
    # left, right, etc.)
    #
    def _move_forward(self, x):
        if self.debug:
            print(f'moving forward by {x}')
        self.tello.move_forward(x)

    def _move_back(self, x):
        if self.debug:
            print(f'moving back by {x}')
        self.tello.move_back(x)

    def _move_left(self, x):
        if self.debug:
            print(f'moving left by {x}')
        self.tello.move_left(x)

    def _move_right(self, x):
        if self.debug:
            print(f'moving right by {x}')
        self.tello.move_right(x)

    #
    # Rotation helpers
    #
    def _rotate_clockwise(self, turn=0):
        if self.debug:
            print(f'rotate clockwise {turn} degrees')
        self.tello.rotate_clockwise(turn)

    def _rotate_counter_clockwise(self, turn=0):
        if self.debug:
            print(f'rotate counter clockwise {turn} degrees')
        self.tello.rotate_counter_clockwise(turn)

    #
    # A function that tries to find a mission pad by moving forward each
    # iteration
    #
    def _find_mission_pad(self, direction_func, creep, expected_padid=0,
                          delay_between=None, iteration_limit=None):
        """Finds a mission pad.  This method is passed an ID to the pad being
        looked for, as well as the distance to move. This method takes a
        reference to a "movement function" that is called if the pad is not
        detected.  This pad also takes an optional parameter to limit the
        number of times it iterates looking for the ID.

        Args:
            direction_func (function): A function describing movement. Req.
            creep (int): Distance (in cm) moved. Req.
            expected_padid (int): Pad ID to look for. Req.
            delay_between (float, optional): Optional delay time between
                iterations. Defaults to None.
            iteration_limit (int, optional): Optional limit on the number
                of iterations performed. Defaults to None.
        """
        if self.debug:
            print(f'finding {expected_padid}')
        if not iteration_limit:
            iteration_limit = 1000  # should be longer than flight time
        while iteration_limit != 0 and \
                self.tello.get_mission_pad_id() != expected_padid:
            if self.debug:
                print(f'..iteration {iteration_limit} moving {creep} cm')
            direction_func(creep)
            if delay_between:
                time.sleep(delay_between)
            iteration_limit -= 1

    #
    # excute a singe command..
    #
    def _run_step(self, step_dict):
        # 'delay_after': delay_value is a common parameter to all dict
        # entries.  If specified, the delay_value is used as a delay, otherwise
        # the delay is skipped.
        if 'delay_before' in step_dict:
            delay_value = step_dict['delay_before']
            time.sleep(delay_value)

        # 'step_speed': speed_value (cm/s)
        if 'step_speed' in step_dict:
            step_speed_value = step_dict['step_speed']
            self.tello.set_speed(step_speed_value)
            self.step_speed_override = True

        # 'cmd': 'takeoff'  ??
        if step_dict['cmd'] == 'takeoff':
            self._takeoff()

        # 'cmd': 'land'  ??
        elif step_dict['cmd'] == 'land':
            self._takeoff()

        # 'cmd': 'report_padid'  ??
        elif step_dict['cmd'] == 'report_padid':
            print(f'report_padid: {self.tello.get_mission_pad_id()}')

        # 'cmd': 'rotate', 'direction': 'clockwise', 'angle': value  ?? OR
        # 'cmd': 'rotate', 'direction': 'counter_clockwise', 'angle': value  ??
        elif step_dict['cmd'] == 'rotate':
            direction = step_dict['direction']
            angle = step_dict['value']
            if direction == 'clockwise':
                self._rotate_clockwise(turn=angle)
            elif direction == 'counter_clockwise':
                self._rotate_counter_clockwise(turn=angle)

        # 'cmd': 'move', 'direction': 'up', 'value': value
        # 'cmd': 'move', 'direction': 'down', 'value': value
        # 'cmd': 'move', 'direction': 'left', 'value': value
        # 'cmd': 'move', 'direction': 'right', 'value': value
        # 'cmd': 'move', 'direction': 'forward', 'value': value
        # 'cmd': 'move', 'direction': 'bac', 'value': value
        elif step_dict['cmd'] == 'move':
            direction = step_dict['direction']
            value = step_dict['value']
            if direction == 'up':
                self._move_up(value)
            elif direction == 'down':
                self._move_down(value)
            elif direction == 'left':
                self._move_left(value)
            elif direction == 'right':
                self._move_right(value)
            elif direction == 'forward':
                self._move_forward(value)
            elif direction == 'back':
                self._move_back(value)

        # 'cmd': 'find', 'direction': dir, 'distance': value, 'padid': value
        # where the direction is one of 'forward', 'back', 'left', and 'right'
        elif step_dict['cmd'] == 'find':
            direction = step_dict['direction']
            distance = step_dict['value']
            padid = step_dict['padid']
            delay_between = None
            if 'delay_between' in step_dict:
                delay_between = step_dict['delay_between']
            iteration_limit = None
            if 'iteration_limit' in step_dict:
                iteration_limit = step_dict['iteration_limit']
            if direction == 'forward':
                dir_func = self._move_forward
            elif direction == 'back':
                dir_func = self._move_back
            elif direction == 'left':
                dir_func = self._move_left
            elif direction == 'right':
                dir_func = self._move_right
            self._find_mission_pad(direction_func=dir_func, creep=distance,
                                   expected_padid=padid,
                                   delay_between=delay_between,
                                   iteration_limit=iteration_limit)

        # 'cmd': 'manual'
        # This command can be embedded into the data path to serve as an early
        # (or debug) entrance to manual mode
        elif step_dict['cmd'] == 'manual':
            if self.tello.is_flying:
                self.send_rc_control = True
            # Enable manual
            self.manual_control_init()
            self.manual_control_run()

        if 'delay_after' in step_dict:
            # 'delay_after': delay_value is a common parameter to all dict
            # entries.  If specified, the delay_value is used as a delay,
            # otherwise the delay is skipped.
            delay_value = step_dict['delay_after']
            time.sleep(delay_value)

        if self.step_speed_override:
            # if the speed was overridden during this step, restore it for the
            # next step
            self.tello.set_speed(self.default_speed)
            self.step_speed_override = False

    def run(self):
        # first, execute any AUTO path sequences
        for flight_step in self.flight_path:
            self._run_step(flight_step)

        # Run out of pre-programmed steps, now enable RC control (if flying)
        if self.tello.is_flying:
            self.send_rc_control = True
        # Enable manual
        self.manual_control_init()
        self.manual_control_run()
