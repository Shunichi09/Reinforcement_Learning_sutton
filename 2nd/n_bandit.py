import sys
import numpy as np
import matplotlib.pyplot as plt

class Epsilon_greedy():
    def __init__(self, rate):
        self.random_rate = rate
        self.greedy_rate = 1 - rate

class Greedy():
    def __init__(self):
        self.random_rate = 0
        self.greedy_rate = 1

class Bandit():
    def __init__(self, method_type, bandit_num, arms):
        # パラメータ
        self.method = method_type
        self.arms = arms
        self.bandit_num = bandit_num

        # 各行動に対する報酬の真値
        self.Q_true = np.random.randn(self.bandit_num, self.arms)

        # 推定報酬
        self.Q_esti = np.array([[0.0 for i in range(self.arms)] for j in range(self.bandit_num)])
        self.Q_times = np.array([[0 for i in range(self.arms)] for j in range(self.bandit_num)]) # そのアームを何回引いたか

        # 記録用
        self.sum_rewards = []

    def play(self):# 腕を引きます
        a = self.decide_arm()
        # 行動aが取られた場合の報酬
        reward = []
        for i in range(self.bandit_num):
            reward.append(np.random.normal(self.Q_true[i, a[i]], 1))
        
        sum_reward = sum(reward)/self.bandit_num
        
        self.sum_rewards.append(sum_reward) # 報酬の記録
        self.update_estimate(a, reward)

        return self.sum_rewards

    def decide_arm(self):# どの腕引くか決めます
        a = []
        # 貪欲か貪欲じゃないかの選択
        for i in range(self.bandit_num):
            temp = np.random.rand() * 10
            # print(temp)
            if temp > 10 * self.method.greedy_rate:
                # 探索！（ランダムに選びます）
                a.append(np.random.randint(0, 10))
            else:
                # 貪欲！
                a.append(np.argmax(self.Q_esti[i]))
        
        return a

    def update_estimate(self, a, reward): # 推定値を更新します！
        for i in range(self.bandit_num):
            self.Q_times[i, a[i]] += 1
            self.Q_esti[i, a[i]] = self.Q_esti[i, a[i]] + (1/self.Q_times[i, a[i]])*(reward[i] - self.Q_esti[i, a[i]])


if __name__ == '__main__':
    greedy = Greedy()
    epsilon_greedy_1 = Epsilon_greedy(0.01)
    epsilon_greedy_2 = Epsilon_greedy(0.1)
    
    game_1 = Bandit(greedy, 2000, 10)
    game_2_1 = Bandit(epsilon_greedy_1, 2000, 10)
    game_2_2 = Bandit(epsilon_greedy_2, 2000, 10)

    playtimes = 3000

    for i in range(playtimes):
        rewards_1 = game_1.play()
        rewards_2_1 = game_2_1.play()
        rewards_2_2 = game_2_2.play()

    plt.plot(range(playtimes), rewards_1, 'k', label='greedy')
    plt.plot(range(playtimes), rewards_2_1, 'r', label='epsilon=0.01')
    plt.plot(range(playtimes), rewards_2_2, 'b', label='epsilon=0.1')
    plt.xlabel('play times')
    plt.ylabel('reward')
    plt.grid(True)
    plt.legend()
    plt.show()