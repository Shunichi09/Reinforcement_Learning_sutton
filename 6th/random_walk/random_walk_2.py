import numpy as np
import matplotlib.pyplot as plt
import random
from collections import OrderedDict

class RandomWalk():
    """
    environment model "Random model"
    Attributes
    ------------
    states : list of str
        state of environment
    """
    
    def __init__(self):
        self.states =  ["left_goal", "A", "B", "C", "D", "E", "right_goal"] 

    def state_update(self, state, action):
        """
        Parameters
        ------------
        state : char
            agent position in this game (in this case A-E)
        action : char
            agent action in this game (in this case "right" or "left")
        
        Returns
        ----------
        next_state : char
            agent next position
        temp_reward : int
            temporal (meaning not total) reward 
        """
        end_flg = False
        temp_reward = 0.         

        if action == "left":
            next_state_num = self.states.index(state) - 1
            if self.states[next_state_num] == "left_goal":
                end_flg = True
                temp_reward = 0. # end the game
            
            next_state = self.states[next_state_num]

        elif action == "right":
            next_state_num = self.states.index(state) + 1

            if self.states[next_state_num] == "right_goal":
                end_flg = True
                temp_reward = 1. # clear the game
        
            next_state = self.states[next_state_num]

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
    history_state : list 
        one episode state (this should not have the same state, first visit ES methods)
    values : OrderedDict
        value function
    """

    def __init__(self, step_rate):
        # environment
        self.model = RandomWalk()
        
        self.state = None
        self.states = self.model.states # in this case we shoud know the all states
        self.action_list = ["left", "right"]

        self.step_rate = step_rate # adjust subject
        self.discount_rate = 1.0
        
        # for bootstrap
        self.history_state = None
        self.values = OrderedDict()
        for state in self.states:
            self.values[state] = 0.5

            if state == "left_goal": # in this problem the final state does not have value
                self.values[state] = 0.
            if state == "right_goal":
                self.values[state] = 0.
        
        self. = []

    def train_TD(self, train_num):
        """training the agent TD methods
        Parameters
        -----------
        train_num : int
            training number of reinforcement learning
        """
        for _ in range(train_num):
            self.state = "C" # initial state has been decided

            while True: # Ending this while is worth of ending one episode

                end_flg, next_state, temp_reward = self._play(self.state) # play the game
                # for TD
                self._valuefunc_update_TD(temp_reward, self.state, next_state)

                # save the state and update
                self.history_state.append(self.state)
                self.state = next_state

                if end_flg:
                    break

    def train_montecarlo(self, train_num):
        """training the agent montecarlo methods
        Parameters
        -----------
        train_num : int
            training number of reinforcement learning
        """
        for _ in range(train_num):
            self.state = "C" # initial state has been decided
            self.history_state = []

            while True: # Ending this while is worth of ending one episode
                end_flg, next_state, reward = self._play(self.state) # play the game

                # save the state and update
                # first visit method
                if not self.state in self.history_state:
                    self.history_state.append(self.state)
                
                self.state = next_state

                if end_flg:
                    self._valuefunc_update_montecarlo(reward, self.history_state)
                    break

    def _play(self, state):
        """
        playing the game

        Parameters
        -----------
        state : str
            state of the agent
        """
        action = self._decide_action()
        end_flg, next_state, temp_reward = self.model.state_update(state, action)

        return end_flg, next_state, temp_reward

    def _decide_action(self):
        """
        Returns
        ---------
        action : str
            action of agent
        """

        action = random.choice(self.action_list)

        return action

    def _valuefunc_update_TD(self, reward, state, next_state):
        """
        Parameters
        -----------
        reward : int
            reward the agent got
        state : str 
            now state of agent
        next_state : str 
            next state of agent
        """
        # TD
        self.values[state] = self.values[state] + self.step_rate * (reward + self.discount_rate * self.values[next_state] - self.values[state])

    def _valuefunc_update_montecarlo(self, final_reward, history_state):
        """
        Parameters
        -----------
        reward : int
            reward the agent got
        state : str 
            now state of agent
        next_state : str 
            next state of agent
        """
        # montecarlo
        for state in history_state:
            self.values[state] = self.values[state] + self.step_rate * (final_reward - self.values[state])

    def _calc_RMS(self):
        """calculating RMS

        """




def main():
    # for fig 6.6 
    monte_alphas = [0.01, 0.02, 0.03, 0.04]
    td_alphas = [0.15, 0.1, 0.05]


    plt.legend()
    plt.show()
    

if __name__ == '__main__':
    main()