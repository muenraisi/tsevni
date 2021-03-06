import datetime
import data_api.daily
import base.code
import pandas as pd
import json


class Capital:
    def __init__(self, value=0, account="", cash=0, fund={"000540": [0, 0]}, finance=0, security={}, transfer=0):
        self.value = value
        self.account = account
        self.cash = cash
        self.fund = fund  # net fund and profit fund
        self.finance = finance
        self.security = security
        self.transfer = transfer
        self.cache = None
        self.start_date = datetime.datetime.today()
        self.end_date = datetime.datetime.today()
        self.tmp_days = 15

    def fund_profit(self, date, inverse=False):
        for code in self.fund:
            # print(data_api.daily.get_fund(code, date, date))
            prev_date = date - datetime.timedelta(days=1)
            daily_profit = data_api.daily.get_fund(code, date, date)["daily_profit"][-1]
            if data_api.daily.get_trade_days(date, date):
                self.fund[code][1] = self.fiund[code][0]
            print("monetary fund: ", date.strftime("%Y%m%d"), self.fund, daily_profit,
                  self.fund[code][1] * daily_profit / 10000.)
            self.fund[code][0] += self.fund[code][1] * daily_profit / 10000.

    def operate(self, record, inverse=False):
        operation = record["操作"]
        self.cash += record["发生金额"]
        # print(record)
        if operation == "港股通组合费":
            pass
        elif operation in ["转存管转出", "转存管转入"]:
            pass
        elif operation in ["银行转存", "银行转取"]:  # 入金和出金
            self.transfer += record["发生金额"]
            pass
        elif operation in ["利息归本"]:  # 每季度现金的活期利息
            pass
        elif operation in ["证券理财认购", "证券理财申购"]:
            self.finance -= record["发生金额"]
        elif operation in ["证券理财强行"]:
            self.finance += record["成交数量"]
        elif operation in ["股息红利税补", "股息入账"]:
            pass
        elif operation in ["申购配号", "交收资金冻结", "市值申购中签", "证券交易解冻", "托管转出", "新股入账"]:
            if record["发生金额"] != 0 or record["成交数量"] != 0:
                if operation in ["市值申购中签", "申购配号", "托管转出", "新股入账"]:
                    pass
                else:
                    print("warn: ", operation, record["成交数量"], record["证券名称"], "cost", record["发生金额"])
                # exit(1)
            pass
        elif operation in ["基金资金拨出", "基金资金拨入"]:
            assert (len(self.fund) == 1)
            for code in self.fund:
                self.fund[code][0] -= record["发生金额"]
        elif operation in ["证券买入", "证券卖出", "质押回购拆出", "拆出质押购回"]:
            code = record["证券代码"]
            if code not in self.security:
                self.security[code] = 0
            self.security[code] += record["成交数量"]
            if self.security[code] == 0.0:
                del self.security[code]
        elif operation in ["新股申购确认"]:
            code = record["证券代码"]
            self.security[code] = record["成交数量"]

        else:
            exit("ERROR: unknown operation " + operation)

    def daily_update(self, date, records=pd.DataFrame(), inverse=False):
        self.fund_profit(date, inverse=inverse)
        # print(records)
        for index, record in records.iterrows():
            # print(index)
            self.operate(record, inverse=inverse)

    def compute_value(self, date=datetime.date.today()):
        ret = 0
        ret += self.cash
        for code in self.fund:
            ret += self.fund[code][0] * 1.0
        ret += self.finance
        for code in self.security:
            resolution = base.code.get_security_resolution(code)
            if resolution in ["逆回购", "新股新债"]:  # R-
                price = 100.0
            else:
                if self.cache is None:
                    price = \
                        data_api.daily.get_security(code, date - datetime.timedelta(days=self.tmp_days), date)["close"][
                            -1]
                else:
                    if code not in self.cache:
                        self.cache[code] = data_api.daily.get_security(code, self.start_date - datetime.timedelta(
                            days=self.tmp_days), self.end_date)
                    # print(code,self.cache[code].index)
                    price = self.cache[code][self.cache[code].index <= date]["close"][-1]

            # print(price)
            ret += price * self.security[code]
            print(code, price * self.security[code])
        self.value = ret
        return ret

    def print(self):
        print("value:", self.value)
        print("cash:", self.cash)
        print("fund:", self.fund)
        print("finance:", self.finance)
        print("security", sorted(self.security.items(), key=lambda d:d[0]))
        print("transfer", self.transfer)

    def dump(self, filename="test.json"):
        data = {
            "account": self.account,
            "value": self.value,
            "cash": self.cash,
            "fund": self.fund,
            "finance": self.finance,
            "security": self.security,
            "transfer": self.transfer
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename="test.json"):
        with open(filename, 'r') as f:
            data = json.load(f)
        for key in data:
            setattr(self, key, data[key])

    def enable_cache(self, start_date, end_date, date_format='%Y-%m-%d'):
        self.cache = {}
        if type(start_date) == str:
            self.start_date = datetime.datetime.date(datetime.datetime.strptime(start_date, date_format))
        if type(end_date) == str:
            self.end_date = datetime.datetime.date(datetime.datetime.strptime(end_date, date_format))

    def disable_cache(self):
        self.cache = None

    def reset_cache(self):
        self.cache = {}


if __name__ == "__main__":
    # Load the Pandas libraries with alias 'pd'
    import pandas as pd

    # Read data from file 'filename.csv'
    # (in the same directory that your python process is based)
    # Control delimiters, rows, column names with read_csv (see later)
    df = pd.read_csv("../data/statement/dad/202010.xls", encoding="GB2312", sep='\t', header=0)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.sort_values(by='日期')
    # Preview the first 5 lines of the loaded data
    df_grouped = df.groupby("日期")

    # print(df_grouped.size())

    # test operate function
    # capital = Capital()
    capital = Capital(account="", cash=0, fund={"001621": [0, 0]}, finance=50000, security={})
    all_days = data_api.daily.get_month_days(2020, 10)
    trade_days = data_api.daily.get_trade_days("2020-10-01", "2020-10-31")

    for date in data_api.daily.get_month_days(2020, 10):
        int_date = int(date.strftime("%Y%m%d"))
        if int_date in df_grouped.groups.keys():
            capital.daily_update(date, df_grouped.get_group(int_date))
        else:
            capital.daily_update(date)

    capital.print()
    capital.dump()
    capital = Capital()
    capital.load()
    capital.print()

    print("value is ", capital.value())
