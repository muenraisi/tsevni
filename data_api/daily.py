import warnings
import jqdatasdk
from inspect import currentframe, getframeinfo
import calendar
import base.code
import akshare as ak
import pandas as pd
import datetime

warnings.filterwarnings("ignore")

jqdatasdk.auth('18810883096', 'Ww19930921')
# 查询是否连接成功
is_auth = jqdatasdk.is_auth()


def get_jq_code(stock_code):
    if stock_code[0] == "0" or stock_code[0] == "3":
        return stock_code + ".XSHE"
    elif stock_code[0] == "6":
        return stock_code + ".XSHG"
    else:
        file_info = getframeinfo(currentframe())
        exit(file_info.filename + " " + str(file_info.lineno) + ": unknown stock code " + stock_code)


def get_jq_date(date):
    return date[0:4] + "-" + date[4:6] + "-" + date[6:8]


def get_security(security_code, start_date, end_date, fq="none"):
    resolution = base.code.get_security_resolution(security_code)
    if resolution in ["沪A股", "科创板", "深A股", "中小板", "创业板"]:
        ret = jqdatasdk.get_price(
            get_jq_code(security_code),
            start_date=start_date,
            end_date=end_date,
            fq=fq)
        ret.index = ret.index.map(lambda x: x.to_pydatetime().date())
    elif resolution == "可转债":
        ret = jqdatasdk.bond.run_query(
            jqdatasdk.query(
                jqdatasdk.bond.CONBOND_DAILY_PRICE).filter(
                jqdatasdk.bond.CONBOND_DAILY_PRICE.code == security_code,
                jqdatasdk.bond.CONBOND_DAILY_PRICE.date >= start_date,
                jqdatasdk.bond.CONBOND_DAILY_PRICE.date <= end_date,
            ))
        ret = ret.set_index("date")
    elif resolution == "沪国债":
        ret = ak.bond_zh_hs_daily(symbol="sh" + security_code)
        # pd.to_datetime(ret.index, unit='s')
        # ret.index.map(lambda x: datetime.datetime.fromtimestamp(x))
        ret.index = ret.index.map(lambda x: x.to_pydatetime().date())
        ret = ret[(ret.index >= start_date) & (ret.index <= end_date)]
    elif resolution =="港股通":
        ret = ak.stock_hk_daily(symbol=security_code, adjust="")
        ret.index = ret.index.map(lambda x: x.to_pydatetime().date())
        ret = ret[(ret.index >= start_date) & (ret.index <= end_date)]
    else:
        file_info = getframeinfo(currentframe())
        exit(file_info.filename + " " + str(file_info.lineno) + ": unknown stock code " + security_code)

    # print(type(ret), stock_code, ret)
    if ret.empty:
        file_info = getframeinfo(currentframe())
        exit(file_info.filename + " " + str(file_info.lineno) + ": empty when query " + security_code)
    return ret


def get_fund(fund_code, start_date, end_date):
    ret = jqdatasdk.finance.run_query(
        jqdatasdk.query(
            jqdatasdk.finance.FUND_MF_DAILY_PROFIT).filter(
            jqdatasdk.finance.FUND_MF_DAILY_PROFIT.code == fund_code,
            jqdatasdk.finance.FUND_MF_DAILY_PROFIT.end_date >= start_date,
            jqdatasdk.finance.FUND_MF_DAILY_PROFIT.end_date <= end_date,
        ))
    ret = ret.set_index("end_date")
    # print(type(ret), fund_code, ret)
    assert (not ret.empty)
    return ret


def get_trade_days(start_date, end_date):
    return jqdatasdk.get_trade_days(start_date=start_date, end_date=end_date)


def get_days(start_date, end_date, date_format='%Y-%m-%d'):
    date_list = []
    if type(start_date) == str:
        start_date = datetime.datetime.date(datetime.datetime.strptime(start_date, date_format))
    if type(end_date) == str:
        end_date = datetime.datetime.date(datetime.datetime.strptime(end_date, date_format))
    while start_date <= end_date:
        date_list.append(start_date)
        start_date += datetime.timedelta(days=1)
    return date_list


def get_month_days(year, month):
    """
    返回某年某月的所有日期
    :param year:
    :param month:
    :return:
    """
    date_list = []
    for day in range(calendar.monthrange(year, month)[1] + 1)[1:]:
        date_list.append(datetime.date(year, month, day))
    return date_list


if __name__ == "__main__":
    import datetime

    print("test stock")
    print(get_security("000001", datetime.date.today() - datetime.timedelta(days=5), datetime.date.today()))
    print("test bond")
    print(get_security("123023", datetime.date.today() - datetime.timedelta(days=5), datetime.date.today()))
    print("test monetary fund")
    print(get_fund("000540", datetime.date.today() - datetime.timedelta(days=5), datetime.date.today()))
    print("test 港股通")
    print(get_security("02601", datetime.date.today() - datetime.timedelta(days=5), datetime.date.today()))
