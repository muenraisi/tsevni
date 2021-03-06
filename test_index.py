import warnings
warnings.filterwarnings("ignore")

from jqdatasdk import *
auth('18810883096', 'Ww19930921')
# 查询是否连接成功
is_auth = is_auth()

#获取贵州茅台("600519.XSHG")的所属行业数据
d = get_industry("002110.XSHE",date="2018-06-01")
print(d)




# 查询最近10个交易日申万一级行业指数-钢铁I（801040）的日行情数据。
df=finance.run_query(query(finance.SW1_DAILY_PRICE).filter(finance.SW1_DAILY_PRICE.code=='801040',finance.SW1_DAILY_PRICE.date>='2019-03-01',finance.SW1_DAILY_PRICE.date<='2020-07-01').order_by(finance.SW1_DAILY_PRICE.date.desc()))
df.drop(df.columns[[0,2,3,4,5,6,8,9,10]], axis=1, inplace=True)  # 二维数据两个括号 剔除多余的列

print(df)