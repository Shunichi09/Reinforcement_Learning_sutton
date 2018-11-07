# ブラックジャック
import numpy as np
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

class Player(): # playerの場合
    def __init__(self):
        
        # 持っているカードの和の推移（状態の推移）
        self.player_sum_traj = [np.random.randint(12, 22)]
        # Aceのtraj
        self.Ace_flag_traj = [bool(np.random.choice([0, 1]))]

        if self.Ace_flag_traj[0]:
            self.cards = [self.player_sum_traj[0]-11, 11]
        else:
            temp = np.random.randint(2,10)
            self.cards = [self.player_sum_traj[0]-temp, temp]

        self.init_flag = True

    def play(self):
        stop_flag, score = self._judge_stop()

        while not stop_flag:
            self._draw()
            stop_flag, score = self._judge_stop()          

        return self.player_sum_traj, self.Ace_flag_traj, score # 状態推移，Aceの推移，最終的なscore

    def _judge_stop(self): # ゲーム終了かどうか判断(player)
        # 初期化
        stop_flag = False

        # 和をとる
        score = sum(self.cards)

        if self.init_flag:
            # print('player_sum_traj = {0}'.format(self.player_sum_traj))
            # print('cards = {0}'.format(self.cards))
            
            # 20以上だとplayerはストップ  ここが方策になる
            if score >= 20:
                stop_flag = True

            self.init_flag = False

        else:
            # 大きさ確認
            while 11 in self.cards and score > 21: # 21より大きくてAceを利用する場合
                self.cards[self.cards.index(11)] = 1 # 1を代入
                score = sum(self.cards)

            # 履歴に状態追加
            self.player_sum_traj.append(score)

            # print('player_sum_traj = {0}'.format(self.player_sum_traj))
            # print('cards = {0}'.format(self.cards))
            
            # 20以上だとplayerはストップ  ここが方策になる
            if score >= 20:
                stop_flag = True
            
            # ここでAceを利用しているか判定
            if 11 in self.cards:
                Ace_flag = True
            else:
                Ace_flag = False
            
            # 履歴に追加しておく
            self.Ace_flag_traj.append(Ace_flag)

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
    
    def play(self):
        # 各プレイヤー定義
        self.dealer = Dealer()
        self.player = Player() 

        # 次にプレイヤー
        player_sum_traj, Ace_flag_traj, player_score = self.player.play()

        # まずはディーラー
        open_card, dealer_score = self.dealer.play()

        # judge
        reward = self._reward(dealer_score, player_score)

        '''
        print('player_sum_traj = {0}'.format(player_sum_traj))
        print('opencards = {0}'.format(open_card))
        print('delear_score = {0}'.format(dealer_score))
        print('player_score = {0}'.format(player_score))
        print('reward = {0}'.format(reward))
        print('Ace_flag_traj = {0}'.format(Ace_flag_traj))
        '''

        # 初期訪問MCの場合　同じ状態の蓄積はいらない

        player_sum_traj_unique = player_sum_traj
        Ace_flag_traj_unique = Ace_flag_traj

        ''' 今回は同じ状態にならないのでいりません
        for i in range(len(player_sum_traj)):
            if player_sum_traj[i] not in player_sum_traj_unique:
                player_sum_traj_unique.append(player_sum_traj[i])
                Ace_flag_traj_unique.append(Ace_flag_traj[i])
        '''


        # print('player_sum_traj_unique = {0}'.format(player_sum_traj_unique))
        # print('Ace_flag_traj_unique = {0}'.format(Ace_flag_traj_unique))
        # 値補正
        if open_card == 11: # 11換算でも見えているのはAce
            open_card = 1

        colums = open_card - 1

        # 保存
        for i in range(len(player_sum_traj_unique)):
            if player_sum_traj_unique[i] > 21 or player_sum_traj_unique[i] < 12: # 22以上と11以下はいれてもしょうがないのでパス
                continue
        
            rows = player_sum_traj_unique[i] - 12
            # print(player_sum_traj[i])

            if Ace_flag_traj_unique[i]:
                self.value_state_Ace[rows, colums] += reward
                self.count_value_state_Ace[rows, colums] += 1

            else:
                self.value_state_No_Ace[rows, colums] += reward
                self.count_value_state_No_Ace[rows, colums] += 1
        
        # print('self.value_state_Ace = {0}'.format(self.value_state_Ace))
        # print('self.value_state_No_Ace = {0}'.format(self.value_state_No_Ace))

        return self.value_state_Ace, self.count_value_state_Ace, self.value_state_No_Ace, self.count_value_state_No_Ace
        
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
        self.fig = plt.figure()
        self.axis = self.fig.add_subplot(111, projection='3d')

    def plot_3d(self):
        self.axis.set_xlabel('dealer open card')
        self.axis.set_ylabel('player sum')
        self.axis.set_zlabel('reward')

        X, Y = np.meshgrid(self.x, self.y)
        Z = self.z

        self.axis.plot_surface(X, Y, Z)

        plt.show()

def main():
    game = Blackjack()

    iterations = 500000

    for i in range(iterations):
        print('i = {0}'.format(i))
        value_state_Ace, count_value_state_Ace, value_state_No_Ace, count_value_state_No_Ace = game.play()

    ave_value_state_Ace = value_state_Ace / count_value_state_Ace
    ave_value_state_No_Ace = value_state_No_Ace / count_value_state_No_Ace

    print(np.round(ave_value_state_Ace, 3))
    print(np.round(ave_value_state_No_Ace, 3))

    # 空配列が存在する場合⇒今回はないと想定

    # 3Dplot
    # 軸の作成
    
    x = np.array(range(1, 11)) # sumの状態
    y = np.array(range(12, 22)) # openされているカード

    # 格子に乗る値
    ploter_ace = Ploter_3D(x, y, np.array(ave_value_state_Ace))
    ploter_ace.plot_3d()

    ploter_No_ace = Ploter_3D(x, y, np.array(ave_value_state_No_Ace))
    ploter_No_ace.plot_3d()

if __name__ == '__main__':
    main()


