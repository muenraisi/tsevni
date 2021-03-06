# -*- coding: utf-8 -*-”

import requests
import re

f = open("result.txt", "w", encoding="utf-8")


def re_first_find(re_str, target):
    all_find = re.findall(re_str, target)
    if not all_find:
        return None
    else:
        return all_find[0]


def stock(stock_id="600664", debug=False):
    session = requests.session()
    headers = {
        # pylint: disable=line-too-long
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
    }
    session.headers.update(headers)

    url = "https://www.jisilu.cn/data/stock/" + stock_id
    if debug:
        print(url)
    response = session.get(url)

    response.encoding = "utf-8"
    html = response.text
    # f.write(html)
    # soup = BeautifulSoup(html, "html.parser")
    # soup.find_all("body")[0].find_all("div", "grid data_content")[0].find_all("div", "grid-row")
    '''
    DYR_TTM: Dividend yield rate
    RGR: Revenue growth rate
    PRG: Profit growth rate
    ROE: return of equity
    ILR: Interest-liability ratio
    '''
    stock_dict = dict(close=re_first_find('现价 <span class=\"dc\">(\\d*\\.\\d*)</span>', html),
                      DYR_TTM=re_first_find('股息率<sup>TTM</sup>\\s*.*(\\d+\\.\\d*)%', html),
                      DYR_5Y=re_first_find('<td title="5年平均股息率：(\\d+\\.\\d*)%">', html),
                      ROE_5Y=re_first_find('<td>5年平均ROE <span class="dc">(-*\\d+\\.\\d*)%</span></td>',
                                           html),
                      RGR_5Y=re_first_find('<td>5年营收增长率 <span class="dc">(-*\\d+\\.\\d*)%</span></td>',
                                           html),
                      PGR_5Y=re_first_find('<td title="5年利润复合增长率">\\s*5年利润增长率 <span class="dc">'
                                           '(-*\\d+\\.\\d*)%</span>', html),
                      PGR=re_first_find('<td title="最新报告期归母净利同比增长">\\s*净利同比增长 <span class="dc">'
                                        '(-*\\d+\\.\\d*)%</span>', html),
                      PE=re_first_find('<div class="item_title">PE</div>\\s*<div class="item_desc">当前值：.*'
                                       '(\\d+\\.\\d*)</span></div>', html),
                      PB=re_first_find('<div class="item_title">PB</div>\\s*<div class="item_desc">当前值：.*'
                                       '(\\d+\\.\\d*)</span></div>', html),
                      ILR=re_first_find('有息负债率 <span class="dc">(-*\\d+\\.\\d*)%</span>', html),
                      )
    return stock_dict


if __name__ == '__main__':
    stock_dict = stock()
    bank_file = open("bank.csv", "w", encoding="utf-8")
    bank_file.write("stock_id" + ", ")
    bank_keys = ["DYR_TTM", "DYR_5Y", "PE", "PB", "RGR_5Y", "ROE_5Y", "PGR_5Y", "PGR"]
    for key in bank_keys:
        bank_file.write(key + ", ")
    bank_file.write("\n")
    bank_stocks = ["600016", "601328", "601169", "601988"]

    for stock_id in bank_stocks:
        stock_dict = stock(stock_id=stock_id)
        bank_file.write(stock_id + ", ")
        for key in bank_keys:
            bank_file.write(stock_dict[key] + ", ")
        bank_file.write("\n")
