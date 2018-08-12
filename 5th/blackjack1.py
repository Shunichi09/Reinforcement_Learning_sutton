# ブラックジャック
import numpy as np
import matplotlib.pyplot as plt

def cards_range_correcter(card): # 引いたカードはここ通す
    if card == 1:
        card = 11

    if card > 10:
        card = 10
    
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
            stop_flag = self._judge_stop()          

        return self.cards, score # カードの履歴と和を返す

    def _judge_stop(self): # ゲーム終了かどうか判断
        # 初期化
        stop_flag = False
        # 和をとる
        score = sum(self.cards)
        # 大きさ確認
        if self.sum > 21:# 21より大きい場合
            self.cards


        if self.sum >= 17:
            stop_flag = True

        return stop_flag

    def _draw(self): # カードを引く
        draw_card = card_range_correcter(np.random.randint(1, 13))
        self.cards.append()


class Player(): # player
    def __init__(self):
        self.cards = [] # 持っているカード

   def _judge_stop(self): # ゲーム終了かどうか判断
        # 初期化
        stop_flag = False
        # 和をとる
        self.sum = sum(self.cards)
        # 大きさ確認
        if self.sum > 21:# 21より大きい場合
            self.cards

        if self.sum >= 17:
            stop_flag = True

        return stop_flag

    def _draw(self): # カードを引く
        draw_card = card_range_correcter(np.random.randint(1, 13))
        self.cards.append()

class Blackjack():
    def __init__(self):
        # モンテカルロのやつ保存する
        self.value_state = np.array([])

        # 各プレイヤー定義
        self.dealer = Dealer()
        self.player = Player()        
    
    def play(self):
        # まずはディーラー


        # 次にプレイヤー


        # judge


        # 価値計算します


        # 保存
        
    def _reward(self): #価値計算
        if player_score > dealer_score:
            reward = 1
        elif player_score < dealer_score:
            reward = -1
        else:
            reward = 0

        return reward        

    def _judge_game(self): #勝ち負け



        return end_flag
    
    def 



def main():
    # saveするための！
    

    iterations = 10000
    
    for i in range(iterations):
        game = Blackjack()
        while end_flag:

            game.draw()
            game.play()


            game.save()

