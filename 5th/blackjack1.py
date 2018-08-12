# ブラックジャック
import numpy as np
import matplotlib.pyplot as plt

def card_range_correcter(card): # 引いたカードはここ通す
    if card > 10: # 絵札排除
        card = 10
    
    if card == 1: # とりあえずAceは11で計算
        card = 11
    
    return card

class Dealer(): # ディーラーの場合
    def __init__(self):
        # 見えているカード
        self.open = card_range_correcter(np.random.randint(1, 13))
        # ディラーが持っているカード（1枚が見えているカード）
        self.cards = [self.open, card_range_correcter(np.random.randint(1, 13))]
        self.score = None

    def play(self): # ゲームする場合/交互に引くわけではないので，まずはディーラー
        stop_flag = self._judge_stop()

        while not stop_flag:
            self._draw()
            stop_flag, score = self._judge_stop()          

        return self.open, score # 開いてるカードの履歴と最終的なscoreを返す　ディラーなのでこれだけでいい

    def _judge_stop(self): # ゲーム終了かどうか判断
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

    def _draw(self): # カードを引く
        draw_card = card_range_correcter(np.random.randint(1, 13))
        self.cards.append(draw_card)

class Player(): # playerの場合
    def __init__(self):
        self.cards = [] # 持っているカード これは最初2枚もってるから連動しないはず　下2つは個数合うはず
        # 持っているカードの和の推移（状態の推移）
        self.state_traj = []
        # Aceのtraj
        self.traj_Ace_flag = []
    
    def play(self):
        stop_flag = self._judge_stop()

        while not stop_flag:
            self._draw()
            stop_flag, Ace_flag, score = self._judge_stop()          

        return Ace_flag, self.state_traj, score # Aceを11として使用したか、状態推移、最終的なscore

    def _judge_stop(self): # ゲーム終了かどうか判断
        # 初期化
        stop_flag = False

        # 和をとる
        score = sum(self.cards)

        # 大きさ確認
        while 11 in self.cards and score > 21: # 21より大きくてAceを利用する場合
            self.cards[self.cards.index(11)] = 1 # 1を代入
            score = sum(self.cards)

        # 履歴に状態追加
        self.state_traj.append(score)
        
        # 20以上だとplayerはストップ
        if score >= 20:
            stop_flag = True
        
        # ここでAceを利用しているか判定
        if 11 in self.cards:
            Ace_flag = True
        else:
            Ace_flag = False
        
        # 履歴に追加しておく
        self.traj_Ace_flag.append(Ace_flag)

        return stop_flag, Ace_flag, score

    def _draw(self): # カードを引く
        draw_card = card_range_correcter(np.random.randint(1, 13))
        self.cards.append(draw_card)

class Blackjack():
    def __init__(self):
        # モンテカルロのやつ保存する
        # 3次元配列
        # 1→Aceあり
        # 0→Aceなし
        self.value_state = np.zeros((2, 10, 10))

        # 各プレイヤー定義
        self.dealer = Dealer()
        self.player = Player()        
    
    def play(self):
        # まずはディーラー
        open_card, dealer_score = self.dealer.play()

        # 次にプレイヤー
        traj_Ace_flag, state_traj, player_score = self.player.play()

        # judge
        reward = self._reward(dealer_score, player_score)

        # 保存

        
    def _reward(self, dealer_score, player_score): #価値計算
        if player_score > dealer_score: # player勝ち
            reward = 1
        elif player_score < dealer_score: # dealer勝ち
            reward = -1
        else:
            reward = 0 # 引き分け

        return reward        

def main():
    game = Blackjack()

    iterations = 10000

    for i in range(iterations):
        state_value = game.play()

    # 3Dplot

if __name__ == '__main__':
    main()


