import numpy as np
import matplotlib.pyplot as plt
import random

class WindField():
    """
    environment wind map

    Attributes
    ------------
    map_row_size : int
        row size of the map
    map_colum_size : int
        coulum size of the map
    wind_map : numpy.ndarray
        wind map
    """
    def __init__(self):
        self.map_colum_size = 10
        self.map_row_size = 7
        self.wind_map = np.zeros((self.map_row_size, self.map_colum_size))
        # set the winds
        for i, wind in enumerate([0, 0, 0, 1, 1, 1, 2, 2, 1, 0]):
            self.wind_map[:, i] = wind

        print(self.wind_map)

    def state_update(self, state, action):
        """
        state update with agent action

        Parameters
        ------------
        action : str
            agent action the action must be chosen from ["right", "left", "down", "up"]
        
        Returns
        ------------
        next_state : numpy.ndarray
            new position of agent 
        temp_reward : int
            temporal reward result of agent action
        end_flg : bool
            flagment of goal
        """
        next_state = np.zeros_like(state)
        end_flg = False

        if action == "left":
            # row
            next_state[0] = min(self.wind_map[state[0], state[1]] + state[0], self.map_row_size-1)
            # colum
            next_state[1] = max(state[1] - 1, 0)

        elif action == "right":
            # row
            next_state[0] = min(self.wind_map[state[0], state[1]] + state[0], self.map_row_size-1)
            # colum
            next_state[1] = min(state[1] + 1, self.map_colum_size-1)

        elif action == "up":
            # row
            next_state[0] = min(self.wind_map[state[0], state[1]] + state[0] + 1, self.map_row_size-1)
            # colum
            next_state[1] = state[1]

        elif action == "down":
            # row
            temp = min(self.wind_map[state[0], state[1]] + state[0] - 1, self.map_row_size-1)
            next_state[0] = max(temp, 0)
            # colum
            next_state[1] = state[1] 
        
        # judge the goal
        if next_state[0] == 3 and next_state[1] == 7:
            print("goal!")
            temp_reward = 0.
            end_flg = True
        else:
            temp_reward = -1.

        
        return end_flg, next_state, temp_reward

class Agent():
    """
    Agent model of reinforcement learning

    Attributes
    ------------
    state : str 
        now state of agent
    states : list of str
        state of environment
    action_list : list of str
        agent possibile action list 
    step rate : float
        learning rate of reinforcement learning
    discount rate : float
        discount rate of reward
    action_values : numpy.ndarray
        avtion value function
    """

    def __init__(self):
        # environment
        self.model = WindField()
        
        self.state = None
        self.action_list = np.array(["left", "right", "up", "down"])

        self.step_rate = 0.5 # adjust subject
        self.discount_rate = 1.0
        
        # for bootstrap
        self.history_state = None
        self.action_values = np.zeros((self.model.map_row_size, self.model.map_colum_size, len(self.action_list))) # map size and each state have 4 action

    def train_TD(self, max_train_num):
        """
        training the agent by TD Sarsa
        
        Parameters
        -----------
        max_train_num : int
            training iteration num
        """
        train_num = 0
        history_episode = []

        while (train_num<max_train_num):
            # initial state
            self.state = [3, 0]
            end_flg = False
            # play
            action = self._decide_action(self.state)

            while True: # if break the episode have finished
                
                end_flg, next_state, temp_reward = self._play(self.state, action)
                next_action = self._decide_action(next_state)
                self._action_valuefunc_update(temp_reward, self.state, action, next_state, next_action)

                # update the history
                history_episode.append(train_num)

                if end_flg:
                    break

                # update
                self.state = next_state
                action = next_action
            
            train_num += 1

        return history_episode
    
    def calc_opt_policy(self):
        """
        calculationg optimized policy

        Returns
        ---------
        opt_policy : list of action

        """
        # initial state
        self.state = [3, 0]
        end_flg = False
        history_opt_policy = []
        history_opt_state = []

        while True: # if break the episode have finished

            # play
            action = self._decide_action(self.state, greedy_rate=0)
            end_flg, next_state, temp_reward = self._play(self.state, action)
    
            # save
            history_opt_policy.append(action)
            history_opt_state.append(self.state)

            if end_flg:
                break

            # update
            self.state = next_state

        history_opt_state.append(next_state)

        return history_opt_policy, np.array(history_opt_state)
    
    def _play(self, state, action):
        """
        playing the game

        Parameters
        -----------
        state : str
            state of the agent
        action : str
            action of agent
        """
        end_flg, next_state, temp_reward = self.model.state_update(state, action)

        return end_flg, next_state, temp_reward

    def _decide_action(self, state, greedy_rate=0.1):
        """
        Parameters
        -----------
        state : numpy.ndarray
            now state of agent
        greedy_rate : float
            greedy_rate, default is 0.1

        Returns
        ---------
        action : str
            action of agent
        """
        choice = random.choice([i for i in range(10)])
        
        if choice > (10 * greedy_rate - 1): # greedy, greedy rate is 0.1
            action_value = self.action_values[state[0], state[1], :]

            # this is the point
            actions = self.action_list[np.where(action_value == np.max(action_value))] # max index            
            action = random.choice(actions)

        else: # random
            action = random.choice(self.action_list)

        return action

    def _action_valuefunc_update(self, reward, state, action, next_state, next_action):
        """
        Parameters
        -----------
        reward : int
            reward the agent got
        state : str 
            now state of agent
        action : str 
            action of agent
        next_state : str 
            next state of agent
        next_action : str 
            next action of agent
        """

        print("action : {0} next_action : {1} \n now state : {2} next_state : {3}".format(action, next_action, state, next_state))

        # TD
        self.action_values[state[0], state[1], list(self.action_list).index(action)] =\
                self.action_values[state[0], state[1], list(self.action_list).index(action)] +\
                self.step_rate *\
                (reward + self.discount_rate * self.action_values[next_state[0], next_state[1], list(self.action_list).index(next_action)] -\
                self.action_values[state[0], state[1], list(self.action_list).index(action)])


def main():
    # training
    agent = Agent()
    history_episode = agent.train_TD(170)

    fig1 = plt.figure()
    axis1 = fig1.add_subplot(111)

    axis1.plot(range(len(history_episode)), history_episode)
    axis1.set_xlabel("time step")
    axis1.set_ylabel("episode")

    # calc opt path
    history_opt_policy, history_opt_state = agent.calc_opt_policy()

    print("opt policy is = {0}".format(history_opt_policy))

    print("opt state is = {0}".format(history_opt_state))

    fig2 = plt.figure()
    axis2 = fig2.add_subplot(111)

    axis2.plot(history_opt_state[:, 1]+0.5, history_opt_state[:, 0]+0.5, marker=".")
    axis2.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    main()

