
import numpy as np


class RL_controller:
    def __init__(self, args):
        self.gamma = args.gamma
        self.lr = args.lr
        self.Q_value = np.zeros((args.theta_discrete_steps, args.theta_dot_discrete_steps, 3)) # state-action values
        self.V_values = np.zeros((args.theta_discrete_steps, args.theta_dot_discrete_steps)) # state values
        self.prev_a = 0 # previous action
        # Use a previous_state = None to detect the beginning of the new round e.g. if not(self.prev_s is None): ...
        self.prev_s = None # Previous state

    def reset(self):
        self.prev_a = 0
        self.prev_s = None


    def get_action(self, state, image_state, random_controller=False, episode=0):

        terminal, timestep, theta, theta_dot, reward = state
        random_action_threshold = 0.8  # Fixed probability for taking a random action
        cutoff_episode = 5 # Define a cutoff episode number: after this point, there are definitively no more random actions

        
        # Use random action only if below the cutoff episode number
        if random_controller and (episode < cutoff_episode and np.random.rand() > random_action_threshold):
            action = np.random.randint(0, 3)  # Random action
        else:
            action = np.argmax(self.Q_value[theta, theta_dot])
             # Best action based on Q values

        # Update Q values only if the previous state is not None and not equal to the current state
        if not (self.prev_s is None or self.prev_s == [theta, theta_dot]):
            prev_theta, prev_theta_dot = self.prev_s
            old_value = self.Q_value[prev_theta, prev_theta_dot, self.prev_a]
            next_max = np.max(self.Q_value[theta, theta_dot])
            new_value = (1 - self.lr) * old_value + self.lr * (reward + self.gamma * next_max)
            

            self.Q_value[prev_theta, prev_theta_dot, self.prev_a] = new_value

        # Updating State values; although reducing performance, this is implemented for testing
        for i in range(self.Q_value.shape[0]):  # Iterate over theta
            for j in range(self.Q_value.shape[1]):  # Iterate over theta_dot
                self.V_values[i, j] = np.max(self.Q_value[i, j])

        if episode > cutoff_episode:
            print("Final Matrix: ")
            print(self.V_values)

        self.prev_s = [theta, theta_dot]
        self.prev_a = action
        return action



