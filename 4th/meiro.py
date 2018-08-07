import numpy as np
import matplotlib.pyplot as plt

# Dynamic Program
class Dynamic_program():
    def __init__(self, map_size): # map(numpy), goal(numpy), 
        self.map_size = map_size
        self.map_rows = self.map_size[0] # 行
        self.map_colums = self.map_size[1] # 列
        self.before_V = np.array([[0.0 for i in range(self.map_colums)] for j in range(self.map_rows)])

    def update(self, policy):
        # それぞれの行動分回す（状態遷移確率はない）
        New_V = np.array([[0.0 for i in range(self.map_colums)] for j in range(self.map_rows)])

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
                for action in policy.actions:
                    # 次に移る状態がきまる
                    next_state_row, next_state_colum = self.calc_next_state(i, k, policy.actions_move[action])# 行と列とアクション
                    
                    # 報酬計算
                    reward = self.decide_reward(next_state_row, next_state_colum)

                    # 評価を計算 
                    sum_eval += policy.actions_rate[action]*(reward + self.before_V[next_state_row, next_state_colum])

                # 計算した報酬を代入
                New_V[i, k] = sum_eval                             
        # 更新
        self.before_V = New_V

        return New_V 

    def decide_reward(self, next_state_row, next_state_colum): # 報酬計算
        # 報酬決定(今回はすべてに対して-1)
        reward = -1
        
        return reward

    def calc_next_state(self, i, k, action): # 状態遷移チェック　範囲外なら元に戻す
        next_state_row = i + action[0] # 行
        next_state_colum = k + action[1] # 列

        if next_state_colum > self.map_colums-1:
            next_state_colum = self.map_colums -1

        if next_state_colum < 0:
            next_state_colum = 0

        if next_state_row > self.map_rows -1:
            next_state_row = self.map_rows -1

        if next_state_row < 0:
            next_state_row = 0
        
        return next_state_row, next_state_colum

class Policy():# 方策定義
    def __init__(self):
        self.actions = ['up', 'down', 'right', 'left']
        # 方策の確率
        self.actions_rate = {}
        self.actions_rate['up'] = 0.25
        self.actions_rate['down'] = 0.25
        self.actions_rate['right'] = 0.25
        self.actions_rate['left'] = 0.25

        # 動作
        self.actions_move = {}
        self.actions_move['up'] = [-1, 0]
        self.actions_move['down'] = [1, 0]
        self.actions_move['right'] = [0, 1]
        self.actions_move['left'] = [0, -1]

def main():
    iterations = 3
    policy = Policy()
    map_size = [4, 4]
    dynamic_program = Dynamic_program(map_size, )

    for i in range(iterations):
        V_s = dynamic_program.update(policy)
        print(V_s)


if __name__ == '__main__':
    main()

        