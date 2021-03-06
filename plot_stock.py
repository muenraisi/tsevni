# 参考博文：https://blog.csdn.net/PeakGao/article/details/105634317?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-5.nonecase
# 参考博文博主：peakgao
# auther：懒兔子
# 编程环境：anaconda - Jupyter notebook
import matplotlib.pyplot as plt  # 绘图
import matplotlib.ticker as ticker  # 日期刻度定制
import pandas as pd
import tushare as ts
from matplotlib import colors as mcolors  # 渲染顶点颜色格式
from matplotlib.collections import LineCollection, PolyCollection

pro = ts.pro_api("c304c3c044f037fd4410a2c40d1e8f066db815c299cebfa9e58ae877")
# API括号内，请输入自己的‘tushare token’哦，申请方法详见上上篇懒兔子的博文：量化之路-数据采集-从tushareAPI获取股票数据信息并导出至excel
# tushare介绍博文链接:https://zhuanlan.zhihu.com/p/149754616

from jqdatasdk import *

auth('18810883096', 'Ww19930921')
# 查询是否连接成功
is_auth = is_auth()

start_date = '20190419'
end_date = '20200726'


def dash_date(date):
    return date[0:4] + "-" + date[4:6] + "-" + date[6:8]


#stock_id = '600507.SH'
stock_id = '002110.SZ'
df = ts.pro_bar(api=pro, ts_code=stock_id, adj='qfq', start_date='20190419', end_date='20200726')
df.drop(df.columns[[0, 6, 7, 8, 10]], axis=1, inplace=True)  # 二维数据两个括号 剔除多余的列
print(df)

df_hs300 = ts.get_hist_data('hs300', start=dash_date(start_date), end=dash_date(end_date))
#print(df_hs300)

# 查询最近10个交易日申万一级行业指数-钢铁I（801040）的日行情数据。
df_indus = finance.run_query(
    query(finance.SW1_DAILY_PRICE).filter(
        finance.SW1_DAILY_PRICE.code == '801040',
        finance.SW1_DAILY_PRICE.date >= dash_date(start_date),
        finance.SW1_DAILY_PRICE.date <= dash_date(end_date)).order_by(
        finance.SW1_DAILY_PRICE.date.desc()).limit(1000))
df_indus.drop(df_indus.columns[[0, 2, 3, 4, 5, 6, 8, 9, 10]], axis=1, inplace=True)  # 二维数据两个括号 剔除多余的列
#print(df_indus)


# 在k线基础上计算MACD，并将结果存储在df上面(dif,dea,bar)
def calc_macd(df, fastperiod=12, slowperiod=26, signalperiod=9):
    ewma12 = df['close'].ewm(span=fastperiod, adjust=False).mean()
    ewma26 = df['close'].ewm(span=slowperiod, adjust=False).mean()
    df['dif'] = ewma12 - ewma26
    df['dea'] = df['dif'].ewm(span=signalperiod, adjust=False).mean()
    df['bar'] = (df['dif'] - df['dea']) * 2
    return df


# 在k线基础上计算KDF，并将结果存储在df上面(k,d,j)
def calc_kdj(df):
    low_list = df['low'].rolling(9, min_periods=9).min()
    low_list.fillna(value=df['low'].expanding().min(), inplace=True)
    high_list = df['high'].rolling(9, min_periods=9).max()
    high_list.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100
    df['k'] = pd.DataFrame(rsv).ewm(com=2).mean()
    df['d'] = df['k'].ewm(com=2).mean()
    df['j'] = 3 * df['k'] - 2 * df['d']
    df['kdj'] = 0
    series = df['k'] > df['d']
    df.loc[series[series == True].index, 'kdj'] = 1
    df.loc[series[(series == True) & (series.shift() == False)].index, 'kdjcross'] = 1
    df.loc[series[(series == False) & (series.shift() == True)].index, 'kdjcross'] = -1
    return df


df = df.sort_values(by='trade_date', ascending=True)

# 用的Juppyter notebook，此处断点查看下获取的数据整理状况

# 日期转换成整数序列
date_tickers = df.trade_date.values
df.trade_date = range(0, len(df))  # 日期改变成序号
matix = df.values  # 转换成绘制蜡烛图需要的数据格式(date, open, close, high, low, volume)
xdates = matix[:, 0]  # X轴数据(这里用的天数索引)

# 设置外观效果
plt.rc('font', family='Microsoft YaHei')  # 用中文字体，防止中文显示不出来
plt.rc('figure', fc='k')  # 绘图对象背景图
plt.rc('text', c='#ffffff')  # 文本颜色
plt.rc('axes', axisbelow=True, xmargin=0, fc='k', ec='#ffffff', lw=1.5, labelcolor='#ffffff',
       unicode_minus=False)  # 坐标轴属性(置底，左边无空隙，背景色，边框色，线宽，文本颜色，中文负号修正)
plt.rc('xtick', c='#ffffff')  # x轴刻度文字颜色
plt.rc('ytick', c='#ffffff')  # y轴刻度文字颜色
plt.rc('grid', c='#ffffff', alpha=0.9, ls=':', lw=0.8)  # 网格属性(颜色，透明值，线条样式，线宽)
plt.rc('lines', lw=0.8)  # 全局线宽

mumber_subplot = 2

# 创建绘图对象和4个坐标轴
fig = plt.figure(figsize=(16, 8))
left, width = 0.05, 0.9
ax1 = fig.add_axes([left, 0.95 - 0.9 * 0.35 / (0.35 + 0.15 * (mumber_subplot - 1)), width,
                    0.9 * 0.35 / (0.35 + 0.15 * (mumber_subplot - 1))])  # left, bottom, width, height
ax2 = fig.add_axes(
    [left, 0.95 - 0.9 * 0.35 / (0.35 + 0.15 * (mumber_subplot - 1)) - 0.9 * 0.15 / (0.35 + 0.15 * (mumber_subplot - 1)),
     width, 0.9 * 0.15 / (0.35 + 0.15 * (mumber_subplot - 1))], sharex=ax1)  # 共享ax1轴

plt.setp(ax1.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示


# 绘制蜡烛图
def format_date(x, pos=None): return '' if x < 0 or x > len(date_tickers) - 1 else date_tickers[
    int(x)]  # 日期格式化函数，根据天数索引取出日期值


ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))  # 设置自定义x轴格式化日期函数
ax1.xaxis.set_major_locator(ticker.MultipleLocator(max(int(len(df) / 15), 5)))  # 横向最多排15个左右的日期，最少5个，防止日期太拥挤
opens, closes, highs, lows = matix[:, 1], matix[:, 2], matix[:, 3], matix[:, 4]  # 取出ochl值
avg_dist_between_points = (xdates[-1] - xdates[0]) / float(len(xdates))  # 计算每个日期之间的距离
delta = avg_dist_between_points / 4.0  # 用于K线实体(矩形)的偏移坐标计算
barVerts = [((date - delta, open), (date - delta, close), (date + delta, close), (date + delta, open)) for
            date, open, close in zip(xdates, opens, closes)]  # 生成K线实体(矩形)的4个顶点坐标
rangeSegLow = [((date, low), (date, min(open, close))) for date, low, open, close in
               zip(xdates, lows, opens, closes)]  # 生成下影线顶点列表
rangeSegHigh = [((date, high), (date, max(open, close))) for date, high, open, close in
                zip(xdates, highs, opens, closes)]  # 生成上影线顶点列表
rangeSegments = rangeSegLow + rangeSegHigh  # 上下影线顶点列表
cmap = {True: mcolors.to_rgba('#000000', 1.0),
        False: mcolors.to_rgba('#54fcfc', 1.0)}  # K线实体(矩形)中间的背景色(True是上涨颜色，False是下跌颜色)
inner_colors = [cmap[opn < cls] for opn, cls in zip(opens, closes)]  # K线实体(矩形)中间的背景色列表
cmap = {True: mcolors.to_rgba('#ff3232', 1.0),
        False: mcolors.to_rgba('#54fcfc', 1.0)}  # K线实体(矩形)边框线颜色(上下影线和后面的成交量颜色也共用)
updown_colors = [cmap[opn < cls] for opn, cls in zip(opens, closes)]  # K线实体(矩形)边框线颜色(上下影线和后面的成交量颜色也共用)列表
ax1.add_collection(LineCollection(rangeSegments, colors=updown_colors, linewidths=0.5,
                                  antialiaseds=False))  # 生成上下影线的顶点数据(颜色，线宽，反锯齿，反锯齿关闭好像没效果)
ax1.add_collection(PolyCollection(barVerts, facecolors=inner_colors, edgecolors=updown_colors, antialiaseds=False,
                                  linewidths=0.5))  # 生成多边形(矩形)顶点数据(背景填充色，边框色，反锯齿，线宽)

# 均线
mav_colors = ['#ffffff', '#d4ff07', '#ff80ff', '#00e600', '#02e2f4', '#ffffb9', '#2a6848']  # 均线循环颜色
mav_period = [5, 10, 20, 30, 60, 120, 180]  # 定义要绘制的均线周期，可增减
n = len(df)
for i in range(len(mav_period)):
    if n >= mav_period[i]:
        mav_vals = df['close'].rolling(mav_period[i]).mean().values
        ax1.plot(xdates, mav_vals, c=mav_colors[i % len(mav_colors)], label='MA' + str(mav_period[i]))

# plot hs300 index
hs300_norm = df_hs300['close'] / df_hs300['close'].values[-1] * df['close'].values[0]
ax1.plot(list(df_hs300.T)[::-1], hs300_norm[::-1], marker='+', linestyle='--', linewidth=1, markersize=4, label="hs300")

# plot industry index
indus_norm = df_indus["close"] / df_indus['close'].values[-1] * df['close'].values[0]
ax1.plot(list(df_hs300.T)[::-1],  indus_norm[::-1], color="grey", marker='o', linestyle='-', linewidth=1, markersize=4, label="industry")

ax1.set_title('K线图')  # 标题
ax1.grid(True)  # 画网格
ax1.legend(loc='upper left')  # 图例放置于右上角
ax1.xaxis_date()  # 好像要不要效果一样？

# 成交量和成交量均线（5日，10日）
# ax2.bar(xdates, matix[:, 5], width= 0.5, color=updown_colors) # 绘制成交量柱状图
barVerts = [((date - delta, 0), (date - delta, vol), (date + delta, vol), (date + delta, 0)) for date, vol in
            zip(xdates, matix[:, 5])]  # 生成K线实体(矩形)的4个顶点坐标
ax2.add_collection(PolyCollection(barVerts, facecolors=inner_colors, edgecolors=updown_colors, antialiaseds=False,
                                  linewidths=0.5))  # 生成多边形(矩形)顶点数据(背景填充色，边框色，反锯齿，线宽)
if n >= 5:  # 5日均线，作法类似前面的均线
    vol5 = df['vol'].rolling(5).mean().values
    ax2.plot(xdates, vol5, c='y', label='VOL5')
if n >= 10:  # 10日均线，作法类似前面的均线
    vol10 = df['vol'].rolling(10).mean().values
    ax2.plot(xdates, vol10, c='w', label='VOL10')
ax2.yaxis.set_ticks_position('right')  # y轴显示在右边
ax2.legend(loc='upper right')  # 图例放置于右上角
ax2.grid(True)  # 画网格
# ax2.set_ylabel('成交量') # y轴名称


if mumber_subplot >= 3:
    calc_macd(df)  # 计算MACD
    # MACD
    ax3 = fig.add_axes([left, 0.25, width, 0.2], sharex=ax1)  # 共享ax1轴
    plt.setp(ax3.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
    difs, deas, bars = matix[:, 6], matix[:, 7], matix[:, 8]  # 取出MACD值
    ax3.axhline(0, ls='-', c='g', lw=0.5)  # 水平线
    ax3.plot(xdates, difs, c='w', label='DIFF')  # 绘制DIFF线
    ax3.plot(xdates, deas, c='y', label='DEA')  # 绘制DEA线
    # ax3.bar(xdates, df['bar'], width= 0.05, color=bar_colors) # 绘制成交量柱状图(发现用bar绘制，线的粗细不一致，故使用下面的直线列表)
    cmap = {True: mcolors.to_rgba('r', 1.0), False: mcolors.to_rgba('g', 1.0)}  # MACD线颜色，大于0为红色，小于0为绿色
    bar_colors = [cmap[bar > 0] for bar in bars]  # MACD线颜色列表
    vlines = [((date, 0), (date, bars[date])) for date in range(len(bars))]  # 生成MACD线顶点列表
    ax3.add_collection(
        LineCollection(vlines, colors=bar_colors, linewidths=0.5, antialiaseds=False))  # 生成MACD线的顶点数据(颜色，线宽，反锯齿)
    ax3.legend(loc='upper right')  # 图例放置于右上角
    ax3.grid(True)  # 画网格

if mumber_subplot >= 4:
    # KDJ
    calc_kdj(df)  # 计算KDJ
    ax4 = fig.add_axes([left, 0.05, width, 0.2], sharex=ax1)  # 共享ax1轴
    plt.setp(ax2.get_xticklabels(), visible=False)  # 使x轴刻度文本不可见，因为共享，不需要显示
    K, D, J = matix[:, 9], matix[:, 10], matix[:, 11]  # 取出KDJ值
    ax4.axhline(0, ls='-', c='g', lw=0.5)  # 水平线
    ax4.yaxis.set_ticks_position('right')  # y轴显示在右边
    ax4.plot(xdates, K, c='y', label='K')  # 绘制K线
    ax4.plot(xdates, D, c='c', label='D')  # 绘制D线
    ax4.plot(xdates, J, c='m', label='J')  # 绘制J线
    ax4.legend(loc='upper right')  # 图例放置于右上角
    ax4.grid(True)  # 画网格

# set useblit = True on gtkagg for enhanced performance
from matplotlib.widgets import Cursor  # 处理鼠标

cursor = Cursor(ax1, useblit=True, color='w', linewidth=0.5, linestyle='--')

plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
plt.margins(0,0)

plt.savefig("C:\\Users\\shuai\\Desktop\\filename.png",bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0, facecolor="#000000")
plt.show()
