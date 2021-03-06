# coding=utf-8
from html.parser import HTMLParser

import urllib.request as urllib2
import sys

type = sys.getfilesystemencoding()


# 截止日期
# 每股净资产
# 每股收益
# 每股现金含量
# 每股资本公积金
# 固定资产合计
# 流动资产合计
# 资产总计
# 长期负债合计
# 主营业务收入
# 财务费用
# 净利润
class Stock:
    def __init__(self, line):
        arr = line.split(",")
        self.day = arr[0].replace("-", "") if arr[0] != '-' else '0'  # day(20011231)
        self.NAVPS = arr[2] if arr[2] != '-' else '0'  # 每股净资产 (net assets value per share)
        self.CPS = arr[4] if arr[4] != '-' else '0'  # 每股现金含量 (cash per share)
        self.CRPS = arr[6] if arr[6] != '-' else '0'  # 每股资本公积金 (capital reserve per share)
        self.TFA = arr[8] if arr[8] != '-' else '0'  # 固定资产合计 (total fixed assets)
        self.TCA = arr[10] if arr[10] != '-' else '0'  # 流动资产合计 (total current assets)
        self.TA = arr[12] if arr[12] != '-' else '0'  # 资产总计 (total assets)
        self.TLTI = arr[14] if arr[14] != '-' else '0'  # 长期负债合计 (Total long-term liabilities)
        self.MBR = arr[16] if arr[16] != '-' else '0'  # 主营业务收入 (Main business revenues)
        self.FC = arr[17] if arr[17] != '-' else '0'  # 财务费用 (financial cost)
        self.NP = arr[19] if arr[19] != '-' else '0'  # 净利润 (Net Profit)

    def __repr__(self):
        return """day:%s,NAVPS:%s,CPS:%s,CRPS:%s,TFA:%s,TCA:%s,TA:%s,TLTI:%s,
        MBR:%s,FC:%s,NP:%s""" % (self.day, self.NAVPS,  self.CPS,
                                          self.CRPS, self.TFA, self.TCA, self.TA, self.TLTI,
                                          self.MBR, self.FC, self.NP)


class StockParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.handledtags = ['td']
        self.processing = None
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag in self.handledtags and len(attrs) > 0 and attrs[0][0] == 'align':
            self.processing = tag

    def handle_data(self, data):
        if self.processing:
            self.data.append(data)

    def handle_endtag(self, tag):
        if tag == self.processing:
            self.processing = None


def parse_data(urldata):
    tp = StockParser()
    tp.feed(urldata)
    data = tp.data
    i = 0
    arr = []
    stocks = []
    for row in data:
        arr.append(row.replace(",", "").replace("元", "").replace("\r\n", ""))
        i += 1
        if i % 20 == 0 and i > 0:
            line = ",".join(arr)
            stock = Stock(line)
            stocks.append(stock)
            arr = []
    return stocks


def get_stock(stock_code):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%(" \
          "stock_code)s.phtml?qq-pf-to=pcqq.c2c" % (
              {'stock_code': stock_code})
    print(url)
    req = urllib2.Request(url=url, headers=headers)
    data = urllib2.urlopen(req).read()
    data = data.decode('gbk').replace("&nbsp;", "-")
    # data = unicode(data,'GBK').encode('UTF-8').replace("&nbsp;", "-")
    stocks = parse_data(data)
    return stocks


if __name__ == '__main__':
    stocks = get_stock("600016")
    # print(stocks)
    for stock_finance in stocks:
        print(stock_finance)
