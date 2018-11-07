# ブラックジャック
import numpy as np
# これで割り算を無し
# np.seterr(divide='ignore', invalid='ignore')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

def card_range_correcter(card): # 引いたカードはここ通す
    if card > 10: # 絵札排除
        card = 10
    
    if card == 1: # とりあえずAceは11で計算
        card = 11
    
    return card

class Dealer(): # ディーラーの場合
    def __init__(self):
        # 見えているカード
        self.open = card_range_correcter(np.random.randint(1, 11))
        # ディラーが持っているカード（1枚が見えているカード）
        self.cards = [self.open, card_range_correcter(np.random.randint(1, 14))]

    def play(self): # ゲームする場合/交互に引くわけではないので，まずはディーラー
        stop_flag, score = self._judge_stop()

        while not stop_flag:
            self._draw()
            stop_flag, score = self._judge_stop()          

        return self.open, score # 開いてるカードの履歴と最終的なscoreを返す　ディラーなのでこれだけでいい

    def _judge_stop(self): # ゲーム終了かどうか判断(dealer)
        # 初期化
        stop_flag = False

        # 和をとる
        score = sum(self.cards)

        # 大きさ確認
        while 11 in self.cards and score > 21: # 21より大きくてAceを利用する場合
            self.cards[self.cards.index(11)] = 1 # 1を代入
            score = sum(self.cards)

        # 17以上だとdealerはストップ
        if score >= 17:
            stop_flag = True

        return stop_flag, score

    def _draw(self): # カードを引く(dealer)
        draw_card = card_range_correcter(np.random.randint(1, 14))
        self.cards.append(draw_card)

class Policy():
    def __init__(self):
        # 行がプレイヤーの和（12-21），列がディラーのopenカード（1-10）
        self.ace = np.array([['hit ' for i in range(10)] for k in range(10)])
        self.no_ace = np.array([['hit ' for i in range(10)] for k in range(10)])
        # 初期方策
        self.ace[8:, :] = np.array([['stop' for i in range(10)] for k in range(2)])
        self.no_ace[8:, :] = np.array([['stop' for i in range(10)] for k in range(2)])
    
    def get_action(self, player_sum, Ace_flag, open_card): # opencardは補正済み
        # 値修正
        open_card = open_card - 1
        player_sum = player_sum - 12

        # print(open_card, player_sum)
        
        if Ace_flag:
            return self.ace[player_sum, open_card]
        else:
            return self.no_ace[player_sum, open_card]

    def improve(self, player_sum_traj, Ace_traj, open_card, ave_Q_state_Ace, ave_Q_state_No_Ace):# 状態行動対をもらって方策を改善する
        # print(ave_Q_state_Ace)
        # print(ave_Q_state_No_Ace)
        # open_card = open_card - 1

        for i in range(len(player_sum_traj)):
            if player_sum_traj[i] > 21 or player_sum_traj[i] < 12: # 22以上と11以下はいれてもしょうがないのでパス
                continue

            # 値修正
            player_sum = player_sum_traj[i] - 12

            # print('player_sum = {0}'.format(player_sum_traj[i]))
            # print('open_card = {0}'.format(open_card))

            if Ace_traj[i]:
                # print('ave_Q_state_Ace[player_sum, open_card, 0] = {0}'.format(ave_Q_state_Ace[player_sum, open_card, 0]))
                # print('ave_Q_state_Ace[player_sum, open_card, 1] = {0}'.format(ave_Q_state_Ace[player_sum, open_card, 1]))

                if ave_Q_state_Ace[player_sum, open_card, 0] > ave_Q_state_Ace[player_sum, open_card, 1]:# hitの方が良い場合
                    self.ace[player_sum, open_card] = 'hit '
                elif ave_Q_state_Ace[player_sum, open_card, 0] < ave_Q_state_Ace[player_sum, open_card, 1]:# standの方が良い場合
                    self.ace[player_sum, open_card] = 'stop'
            else:
                # print('ave_Q_state_No_Ace[player_sum, open_card, 0] = {0}'.format(ave_Q_state_No_Ace[player_sum, open_card, 0]))
                # print('ave_Q_state_No_Ace[player_sum, open_card, 1] = {0}'.format(ave_Q_state_No_Ace[player_sum, open_card, 1]))

                if ave_Q_state_No_Ace[player_sum, open_card, 0] > ave_Q_state_No_Ace[player_sum, open_card, 1]:# hitの方が良い場合
                    self.no_ace[player_sum, open_card] = 'hit '
                elif ave_Q_state_No_Ace[player_sum, open_card, 0] < ave_Q_state_No_Ace[player_sum, open_card, 1]:# standの方が良い場合
                    self.no_ace[player_sum, open_card] = 'stop'

class Player(): # playerの場合
    def __init__(self, policy):
        
        # 持っているカードの和の推移（状態の推移）
        self.player_sum_traj = [np.random.randint(12, 22)]
        # Aceのtraj
        self.Ace_flag_traj = [bool(np.random.choice([0, 1]))]
        # Actionのtraj
        self.action_traj = [np.random.choice(['hit ', 'stop'])]

        # print(self.action_traj)

        # 方策
        self.policy = policy

        if self.Ace_flag_traj[0]:
            self.cards = [self.player_sum_traj[0]-11, 11]
        else:
            temp = np.random.randint(2,10)
            self.cards = [self.player_sum_traj[0]-temp, temp]

        self.init_flag = True

    def play(self, open_card): # opencardは補正されてはいってくる
         # dealerのカード
        self.open_card = open_card

        stop_flag, score = self._judge_stop()       

        while not stop_flag:
            self._draw()
            stop_flag, score = self._judge_stop()          

        return self.player_sum_traj, self.Ace_flag_traj, self.action_traj, score # 状態推移，Aceの推移，アクションの推移，最終的なscore

    def _judge_stop(self): # ゲーム終了かどうか判断(player)
        # 初期化
        stop_flag = False

        # 和をとる
        score = sum(self.cards)

        if self.init_flag:
            # print('state_traj = {0}'.format(self.state_traj))
            # print('cards = {0}'.format(self.cards))
            # self.action_traj.append(self.policy.get_action(self.player_sum_traj[0], self.Ace_flag_traj[0], self.open_card))

            # 方策にしたがう
            if self.action_traj[0] == 'stop':
                stop_flag = True

            self.init_flag = False

        else: # 初期状態ではない
            # 大きさ確認
            while 11 in self.cards and score > 21: # 21より大きくてAceを利用する場合
                self.cards[self.cards.index(11)] = 1 # 1を代入
                score = sum(self.cards)

            # ここでAceを利用しているか判定
            if 11 in self.cards:
                Ace_flag = True
            else:
                Ace_flag = False
            
            # print('state_traj = {0}'.format(self.player_sum_traj))
            # print('cards = {0}'.format(self.cards))

            if score > 21:
                stop_flag = True
                return stop_flag, score

            # 履歴に追加しておく
            self.Ace_flag_traj.append(Ace_flag)

            # 履歴に状態追加
            self.player_sum_traj.append(score)

            # print(self.policy.get_action(self.player_sum_traj[-1], self.Ace_flag_traj[-1], self.open_card))

            self.action_traj.append(self.policy.get_action(self.player_sum_traj[-1], self.Ace_flag_traj[-1], self.open_card))

            # 方策にしたがう
            if self.policy.get_action(self.player_sum_traj[-1], self.Ace_flag_traj[-1], self.open_card) == 'stop':
                stop_flag = True
            
        return stop_flag, score

    def _draw(self): # カードを引く(player)
        draw_card = card_range_correcter(np.random.randint(1, 14))
        self.cards.append(draw_card)

class Blackjack():
    def __init__(self):
        # モンテカルロのやつ保存する
        # self.value_state = np.zeros((2, 10, 10))で三次元的にやるのもありですが．．．わかりにくそうなのでやめます
        # 行がプレイヤーの和（12-21），列がディラーのopenカード（1-10）
        self.value_state_Ace = np.array([[0.0 for i in range(10)] for k in range(10)])
        self.value_state_No_Ace = np.array([[0.0 for i in range(10)] for k in range(10)]) # AceとAceなしでそれぞれ状態は10×10あります
        # カウンター
        self.count_value_state_Ace = np.array([[0 for i in range(10)] for k in range(10)])
        self.count_value_state_No_Ace = np.array([[0 for i in range(10)] for k in range(10)]) # AceとAceなしでそれぞれ状態は10×10あります 

        # 行動価値推定
        self.Q_state_Ace = np.array([[[0.0, 0.0] for i in range(10)] for k in range(10)])
        self.Q_state_No_Ace = np.array([[[0.0, 0.0] for i in range(10)] for k in range(10)]) # AceとAceなしでそれぞれ状態は10×10×2あります
        # カウンター
        self.count_Q_state_Ace = np.array([[[0, 0] for i in range(10)] for k in range(10)])
        self.count_Q_state_No_Ace = np.array([[[0, 0] for i in range(10)] for k in range(10)]) # AceとAceなしでそれぞれ状態は10×10あります 
        # 行動価値推定(平均)
        self.ave_Q_state_Ace = np.array([[[0.0, 0.0] for i in range(10)] for k in range(10)])
        self.ave_Q_state_No_Ace = np.array([[[0.0, 0.0] for i in range(10)] for k in range(10)]) # AceとAceなしでそれぞれ状態は10×10×2あります

        # 方策
        self.policy = Policy()
    
    def play(self):
        # 各プレイヤー定義
        self.dealer = Dealer()
        self.player = Player(self.policy) 

        # まずはディーラー(あえて順番逆にしてます)
        open_card, dealer_score = self.dealer.play()

        # 補正
        if open_card == 11: # 11換算でも見えているのはAce
            open_card = 1

        # 次にプレイヤー
        player_sum_traj, Ace_flag_traj, action_traj, player_score = self.player.play(open_card)

        # judge
        reward = self._reward(dealer_score, player_score)

        # print('player_sum_traj = {0}'.format(player_sum_traj))
        # print('open_card = {0}'.format(open_card))
        # print('delear_score = {0}'.format(dealer_score))
        # print('player_score = {0}'.format(player_score))
        # print('reward = {0}'.format(reward))
        # print('Ace_flag_traj = {0}'.format(Ace_flag_traj))
        # print('action_traj = {0}'.format(action_traj))

        # 初期訪問MCの場合　同じ状態の蓄積はいらない

        # 保存
        open_card = open_card - 1

        for i in range(len(player_sum_traj)):
            if player_sum_traj[i] > 21 or player_sum_traj[i] < 12: # 22以上と11以下はいれてもしょうがないのでパス
                continue

            action = action_traj[i]
            if action == 'hit ':
                action = 0
            else:
                action = 1

            player_sum = player_sum_traj[i] - 12
            # print(state_traj[i])

            if Ace_flag_traj[i]:
                self.Q_state_Ace[player_sum, open_card, action] += reward
                self.count_Q_state_Ace[player_sum, open_card, action] += 1

            else:
                self.Q_state_No_Ace[player_sum, open_card, action] += reward
                self.count_Q_state_No_Ace[player_sum, open_card, action] += 1

        # 平均出す
        for i in range(len(player_sum_traj)):
            if player_sum_traj[i] > 21 or player_sum_traj[i] < 12: # 22以上と11以下はいれてもしょうがないのでパス
                continue

            action = action_traj[i]
            if action == 'hit ':
                action = 0
            else:
                action = 1

            player_sum = player_sum_traj[i] - 12
            # print(state_traj[i])

            if Ace_flag_traj[i]:
                self.ave_Q_state_Ace[player_sum, open_card, action] = self.Q_state_Ace[player_sum, open_card, action] / self.count_Q_state_Ace[player_sum, open_card, action]

            else:
                self.ave_Q_state_No_Ace[player_sum, open_card, action] = self.Q_state_No_Ace[player_sum, open_card, action] / self.count_Q_state_No_Ace[player_sum, open_card, action]

        # 方策改善
        self.policy.improve(player_sum_traj, Ace_flag_traj, open_card, self.ave_Q_state_Ace, self.ave_Q_state_No_Ace)

        return self.policy, self.Q_state_Ace, self.count_Q_state_Ace, self.Q_state_No_Ace \
                    , self.count_Q_state_No_Ace, self.ave_Q_state_Ace, self.ave_Q_state_No_Ace 
        
    def _reward(self, dealer_score, player_score): #価値計算
        if player_score > 21: # dealerがくず手の時点で勝ち
            reward = -1.0
        else:
            if dealer_score > 21: # 自分がくず手なら負け 
                reward = 1.0
            else:
                if player_score > dealer_score: # player勝ち
                    reward = 1.0
                elif player_score < dealer_score: # dealer勝ち
                    reward = -1.0
                elif player_score == dealer_score:
                    reward = 0.0 # 引き分け

        return reward
    
# 3Dgraphを作成
class Ploter_3D():
    def __init__(self, x, y, z):
        self.x = x # 1次元可能
        self.y = y # 1次元可能
        self. z = z # 2次元配列でほしい
        # グラフ作成
        # self.fig_3D = plt.figure()
        self.fig_2D = plt.figure()
        #  self.axis_3D = self.fig_3D.add_subplot(111, projection='3d')
        self.axis_2D = self.fig_2D.add_subplot(111)

    '''
    def plot_3d(self):
        self.axis_3D.set_xlabel('dealer open card')
        self.axis_3D.set_ylabel('player sum')
        self.axis_3D.set_zlabel('reward')

        X, Y = np.meshgrid(self.x, self.y)
        Z = self.z

        self.axis_3D.plot_surface(X, Y, Z)

        plt.show()
    '''

    def plot_hit_or_stop(self, title):
        self.axis_2D.set_xlabel('dealer open card')
        self.axis_2D.set_ylabel('player sum')

        self.axis_2D.set_title(title)

        X, Y = np.meshgrid(self.x, self.y)

        Z = self.z

        img = self.axis_2D.pcolormesh(X, Y, Z, cmap='summer')

        pp=self.fig_2D.colorbar(img, orientation="vertical") # カラーバーの表示 
        pp.set_label('label') # カラーバーの表示 

        plt.show()

def main():
    game = Blackjack()

    iterations = 1000000

    for i in range(iterations):
        print('i = {0}'.format(i))
        policy, Q_state_Ace, count_Q_state_Ace, Q_state_No_Ace, count_Q_state_No_Ace, ave_Q_state_Ace, ave_Q_state_No_Ace = game.play()

    print('policy.ace = \n {0}'.format(policy.ace))
    print('policy.no_ace = \n {0}'.format(policy.no_ace))

    # 空配列が存在する場合⇒今回はないと想定

    # 3Dplot
    # 軸の作成
    
    x = np.array(range(1, 11)) # sumの状態
    y = np.array(range(12, 22)) # openされているカード

    # 格子に乗る値
    ploter_ace = Ploter_3D(x, y, np.array(policy.ace == 'hit ', dtype=int))
    ploter_ace.plot_hit_or_stop('with_ace')

    ploter_No_ace = Ploter_3D(x, y, np.array(policy.no_ace == 'hit ', dtype=int))
    ploter_No_ace.plot_hit_or_stop('without_ace')


if __name__ == '__main__':
    main()


