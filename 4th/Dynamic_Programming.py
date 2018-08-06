import numpy as np
import matplotlib.pyplot as plt

# Dynamic Program
class Dynamic_program():
    def __init__(self, map_size, goal): # map(numpy), goal(numpy), 
        self.map_size = map_size
        self.map_rows = self.map_size[0] # 行
        self.map_colums = self.map_size[1] # 列
        self.goal = goal
        self.before_V = np.array([[0.0 for i in range(self.map_size.shape[1])] for k in range(self.map_size.shape[0])])

    def update(self, policy):
        # それぞれの行動分回す（状態遷移確率はない）
        New_V = np.array([[0.0 for i in range(self.map_size.shape[1])] for k in range(self.map_size.shape[0])])

        for i in range(self.map_rows):# 状態をすべて選ぶ イレギュラーですが行からで(これは全探索の意味)
            if i == 0: # 1行目の最終状態は除く
                colums_start = 1
                colums_end = self.map_colums
            elif i == self.map_rows -1: # 最終行の最終状態は除く
                colums_start = 0
                colums_end = self.map_colums -1 
            else: # これはいつもどおり
                colums_start = 0
                colums_end = self.map_colums

            for k in range(colums_start, colums_end):
                # 各状態において計算
                sum_eval = 0.0
                for action in self.actions:
                    # 次に移る状態がきまる
                     next_state_row,  next_state_colum = self.calc_next_state(i, k, action)
                    
                    # 報酬計算
                    reward = self.decide_reward(next_state_row, next_state_colum)

                    # 評価を計算 
                    sum_eval += policy_rate*(reward + self.before_V[next_state_row, next_state_colum])

                # 計算した報酬を代入
                New_V[i, k] = sum_eval                             
        # 更新
        self.before_V = New_V

        return New_V 

    def decide_reward(self, next_state_row, next_state_colum):
        # 報酬決定
        if next_state_row == 0 and next_state_colum == 0: # 次の状態で報酬をチェック
            reward = -1
        elif next_state_row == self.map_rows-1 and next_state_colum == self.map_colums-1:
            reward = -1
        else: 
            reward = 1
        
        return reward

    def calc_next_state(self, i, k, action):
        next_state_row = i + action[0] # 行
        next_state_colum = k + action[1] # 列



class Policy():
    def __init__(self):
        self.actions = ['up', 'down', 'right', 'left']
        # 方策の確率
        self.actions_rate = {}
        self.actions_rate['up'] = 0.25
        self.actions_rate['down'] = 0.25
        self.actions_rate['right'] = 0.25
        self.actions_rate['left'] = 0.25

        # 動作
        self.actions_move['up'] = [-1, 0]
        self.actions_move['down'] = [1, 0]
        self.actions_move['right'] = [0, 1]
        self.actions_move['left'] = [0, -1]

def main():
    iterations = 2000
    policy = Policy()
    dynamic_program = Dynamic_program()

    for i in range(iterations):



if __name__ == '__main__':

        