import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from plotly import graph_objects as go

# x、yデータ
#x = [np.random.randint(255) for i in range(10)]
#y = [np.random.randint(255) for i in range(10)]
#o = [np.random.randint(255) for i in range(10)]

x = [20,40,60,100,180,200]
y = [20,40,60,100,180,200]
o = [20,40,60,100,180,200]

normal = colors.Normalize(vmin=0., vmax=255.)
array_px = [[i,j,k] for (i,j,k) in zip(x,y,o)]
array_px = normal(array_px).tolist()

print(array_px) 
# 点(x, y)がもつ量
#z = range(20)
 
# カラーマップ
#cm = plt.cm.get_cmap('RdYlBu')
# figureを生成する
#fig = plt.figure()
 
# axをfigureに設定する
#ax = fig.add_subplot(1, 1, 1, projection='3d')
 
# axに散布図を描画、戻り値にPathCollectionを得る
#mappable = ax.scatter(x, y, o, color=array_px)
 
# カラーバーを付加
#fig.colorbar(mappable, ax=ax)
 
figure = go.Figure(
    data=[go.Scatter3d(
        x=x,
        y=y,
        z=o,
        mode='markers',
        marker=dict(
            size=10,
            color=array_px
        )
    )]
)

# 表示
figure.show()