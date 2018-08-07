import numpy as np
import matplotlib.pyplot as plt
import copy
import sys

class Gamble():
    def __init__(self):
        # 状態価値関数
        self.V_s = [0.0 for i in range(101)] # 状態は99個 + 最後の状態と最初の状態を追加
        self.V_s[-1] = 1.0 # 最後は報酬+1
        self.old_V_s = [0.0 for i in range(101)] # 状態は99個 + 最後の状態と最初の状態を追加
        self.old_V_s[-1] = 1.0 # 最後は報酬+1
        # 各状態でいくら賭けるか（policy）
        self.policy = [0 for i in range(101)]# 状態は99個 + 最後の状態と最初の状態を追加
        self.coin_rate = 0.4
        self.delta_limit = 1e-5 # 変更量閾値

    def update_V(self):
        delta = 1.0
        count = 0
        while delta >= self.delta_limit:
            count += 1
            delta = 0.0
            for s in range(1, 100):# すべての状態でやる これで1から99まで
                E = 0.0
                
                for i in range(1, min(s, 100-s) + 1):
                    # 期待値計算
                    temp_E = self.coin_rate * self.old_V_s[s + i] + (1.0 - self.coin_rate) * self.old_V_s[s - i]

                    # もっとも大きいものを選ぶ
                    E = max(temp_E, E)

                # 大きい方に合わせる
                delta = max(delta, abs(self.old_V_s[s]-E))
            
                # 更新
                self.V_s[s] = E
            
            self.old_V_s = copy.deepcopy(self.V_s)
            # print(self.V_s)

        print(count)
        
        return self.V_s

    def calc_optimal_policy(self):
        # どれがいいか探します（すべての組み合わせをみて報酬が最大になった行動を返す）
        E = 0.0
        for s in range(1, 100):
            for i in range(1, min(s, 100-s) + 1): # 
                # 期待値計算
                temp_E = self.coin_rate * self.V_s[s + i] + (1.0 - self.coin_rate) * self.V_s[s - i]
                
                if temp_E > E + self.delta_limit:
                    E = temp_E 
                    self.policy[s] = i             

        return self.policy

    def plot(self, axis1, axis2):
        axis1.plot(range(1, 100), self.V_s[1:100]) # 状態価値
        axis2.plot(range(1, 100), self.policy[1:100]) # 最適方策

def main():
    coin = Gamble()

    count = 0

    V_s = coin.update_V()

    # 最適方策を計算
    opt_poliy = coin.calc_optimal_policy()

    figure = plt.figure()
    axis1 = figure.add_subplot(211)
    axis2 = figure.add_subplot(212)
    
    coin.plot(axis1, axis2)

    plt.show()

if __name__ == '__main__':
    main()