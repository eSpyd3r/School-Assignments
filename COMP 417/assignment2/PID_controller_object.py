import numpy as np


class PID_controller:
    def __init__(self, Kp=1.5, Ki=0.0, Kd=1.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0
        self.prev_action = 0 #I didn't end up using this

    def reset_state(self):
        self.prev_error = 0
        self.integral = 0
        self.prev_action = 0

    def get_action(self, state, image_state, random_controller=False):
        #terminal, Boolean
        #timestep, int
        #x, float, [-2.4, 2.4]
        #x_dot, float, [-inf, inf]
        #theta, float, [-pi/2, pi/2], radians
        #theta_dot, float, [-inf, inf]
        #reward, int, 0 or 1
        #image state is a (800, 400, 3) numpy image array

        terminal, timestep, x, x_dot, theta, theta_dot, reward = state



        if random_controller:
            return np.random.uniform(-1, 1)
        else:

            #if np.random.rand() > 0.99:
            #    print("Random action!")
            #    return 10

            error = theta  # Error is the deviation from the vertical position

            # P term
            P = self.Kp * error

            # I term
            self.integral += error
            I = self.Ki * self.integral

            # D term
            D = self.Kd * (error - self.prev_error)
            self.prev_error = error

            # Control action
            action = P + I + D
            return action
