import numpy as np
import matplotlib.pyplot as plt
import random

class RandomWalk():
    """
    environment model "Random model"
    Attributes
    ------------
    state : 

    """
    
    def __init__(self):
        self.states = ["A", "B", "C", "D", "E"]
        self.action = None

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
        temp_reward = 0         

        if action == "left":
            next_state_num = self.states.index(state) - 1
            if next_state_num < 0:
                end_flg = True
                next_state = None
                temp_reward = 0 # end the game
                
            next_state = self.states[next_state_num]

        elif action == "right":
            next_state_num = self.states.index(state) + 1
            if next_state_num >= len(self.states):
                end_flg = True
                next_state = None
                temp_reward = 1 # clear the game

            next_state = self.states[next_state_num]

        return end_flg, next_state, temp_reward

class Agent():
    """
    """

    def __init__(self, init):
        self.state = None
        self.states = ["A", "B", "C", "D", "E"] # in this case we shoud know the all states
        self.action_list = ["left", "right"]
        self.step_rate = 0.1 # adjust subject
        
        self.values = {}
        for state in self.states:
            self.values[state] = 0.5
        
        self.model = RandomWalk()
        
        # for bootstrap
        self.history_state = None

    def train(self, train_num):
        """
        Parameters
        -----------
        train_num : int

        """
        for _ in range(train_num):
            self.state = "C" # initial state has been decided
            self.history_state = []

            while not end_flg: # Ending this while is worth of ending one episode

                self.play()
                # for TD
                self._valuefunc_update()

            # for montecarlo
            self._valuefunc_update()

    def play(self):
        """
        """
        
        action = self._decide_action()

        end_flg, next_state, temp_reward = self.model.state_update(self.state, action)

        # save the state for montecarlo
        if state not in self.history_state: # ES
            self.history_state.append(self.state)

        self.state = next_state

    def _decide_action(self):
        """
        Returns
        ---------
        action : str
            action of agent
        """

        action = random.choice(action_list)

        return action

    def _valuefunc_update(self):
        """
        """
        # montecarlo
        for state in self.history_state:
            values[state] = values[state] + self.step_rate * (final_reward - values[state])

        # TD
        values[state] = values[state] + self.step_rate * (reward + self.discount_rate * values[next_state] - values[state])

def main():





if __name__ == '__main__':
    main()