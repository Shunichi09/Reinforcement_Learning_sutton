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

    def __init__(self):
        # environment
        self.model = RandomWalk()
        
        self.state = None
        self.states = self.model.states # in this case we shoud know the all states
        self.action_list = ["left", "right"]

        self.step_rate = 0.1 # adjust subject
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
                self._valuefunc_update(temp_reward, self.state, next_state)

                # update
                self.state = next_state

                if end_flg:
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

    def _valuefunc_update(self, reward, state, next_state):
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

def main():
    # for fig 6.6 
    # 0
    agent = Agent()
    agent.train_TD(0)
    values = list(agent.values.values())
    plt.plot(range(len(agent.values.keys()) - 2), values[1:-1] , label="0", marker=".")
    # 1
    agent = Agent()
    agent.train_TD(1)
    values = list(agent.values.values())
    plt.plot(range(len(agent.values.keys()) - 2), values[1:-1] , label="1", marker=".")
    # 10
    agent = Agent()
    agent.train_TD(10)
    values = list(agent.values.values())
    plt.plot(range(len(agent.values.keys()) - 2), values[1:-1] , label="10", marker=".")
    # 100
    agent = Agent()
    agent.train_TD(100)
    values = list(agent.values.values())
    plt.plot(range(len(agent.values.keys()) - 2), values[1:-1] , label="100", marker=".")
    # true
    values = np.arange(1/6, 0.9, 1/6)
    print(values)
    plt.plot(range(len(agent.values.keys()) - 2), values, label="True", marker=".")

    plt.legend()
    plt.show()
    

if __name__ == '__main__':
    main()