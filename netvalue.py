# Load the Pandas libraries with alias 'pd'
import pandas as pd
from account.capital import *
import data_api

# Read data from file 'filename.csv'
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later)
account = "me"

df=pd.read_csv("C:\\Users\\shuai\\Documents\\table.xls",encoding="GB2312", sep="\t", header=0,
               dtype={"证券代码":str} )

# df = pd.read_csv("data/statement/" + account + "/202010.xls", encoding="GB2312", sep='\t', header=0)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.sort_values(by='日期')
# Preview the first 5 lines of the loaded data
df_grouped = df.groupby("日期")

# print(df_grouped.size())

# test operate function
# capital = Capital()
security = {
    "00548":2000,
    "01088":1500,
    "01171":4000,
    "01812": 6500,
    "02601": 200,
    '000036': 3510,
    '000429': 2400,
    "000911": 4900,
    "000930": 1900,
    "002003": 3400,
    "002110": 1650,
    "002327": 2600,
    "002394": 2300,
    "002532": 2700,
    "019547": 100,
    "113527": 500,
    "113591": 100,
    "127018": 1100,
    "128062": 100,
    "128085": 100,
    "128093": 200,
    "128127": 200,
    "131810": 400,
    "131811": 230,
    "600080": 3100,
    "600507": 5811,
    "600817": 2100,
    "600873": 6700,
    "600919": 2900,
    "601009": 5000,
    "601318": 300,
    "601838": 3700,
}
capital = Capital(account=account, cash=21302.5, fund={"000540": [930., 930.]}, finance=50000, security=security)
# capital = Capital(account=account, fund={"001621": [0,0]}) # dad
start_date="2020-11-01"
end_date="2020-11-06"



last_date= datetime.date.fromisoformat(start_date)-datetime.timedelta(days=1)
capital.dump("data/backup/captial_" + account + "_"+last_date.strftime("%Y%m%d")+".json")
all_days = data_api.daily.get_days(start_date, end_date)
trade_days = data_api.daily.get_trade_days(start_date, end_date)
capital.enable_cache(start_date, end_date)

net_value = 1.0
for date in all_days:
    print("---start---", date)
    str_date = date.strftime("%Y%m%d")
    int_date = int(str_date)
    capital.transfer = 0
    last_value = capital.value

    if int_date in df_grouped.groups.keys():
        capital.daily_update(date, df_grouped.get_group(int_date))
    else:
        capital.daily_update(date)

    value = capital.compute_value(date)
    if value != 0.0:
        if last_value != 0:
            ror = (value - capital.transfer) / last_value
        else:
            ror = 1.0
        net_value = net_value * ror
        print(last_value, value, net_value, "{:.2%}".format(ror - 1))
        capital.dump("data/capital/"+account+"/"+str_date+".json")

capital.print()
