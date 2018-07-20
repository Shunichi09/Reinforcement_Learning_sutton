import numpy as np
import matplotlib.pyplot as plt

# グラフ作成
fig = plt.figure()

# axis
itiyo_ax = fig.add_subplot(131)
seiki_ax = fig.add_subplot(132)
coins_ax = fig.add_subplot(133)

figures = [itiyo_ax, seiki_ax, coins_ax]

# 一様分布（どれも等確率です）
y_1 = np.random.rand(1000)

# ヒストグラムを書きます
img = itiyo_ax.hist(y_1, bins=10, ec='black')

# 正規分布
y_2 = np.random.randn(1000)

# ヒストグラムを書きます
img = seiki_ax.hist(y_2, bins=20, ec='black')

# 10パーセントで裏，と90パーセントで表の出る確率
count_omote = 0
count_ura = 0

for i in range(1000):#1000回試行します
    temp = np.random.randint(1, 11)
    print(temp)
    if temp > 9:
        count_ura += 1
    else:
        count_omote += 1

print('Omote = {0}'.format(count_omote/1000))
print('Ura = {0}'.format(count_ura/1000))

img = coins_ax.bar([1, 0], [count_omote, count_ura], ec='black')

plt.tight_layout()
plt.show()