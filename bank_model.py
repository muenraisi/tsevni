# -*- coding: utf-8 -*-
__author__ = 'Shuai Wu'

import pandas as pd
import matplotlib.pyplot as plt

import MrCrawl.jsl as jsl
import MrCrawl.industry as industry

dym_ttm_dict = {}

for stock_id in industry.BANK_STOCK:
    stock_dict = jsl.stock(stock_id)
    print(stock_dict)
    dym_ttm_dict[stock_id] = stock_dict["DYR_TTM"]

stock_value = pd.DataFrame.from_dict(dym_ttm_dict, orient='index', dtype="float")
stock_value = stock_value.sort_values(by=[0], ascending=False)
print(stock_value)
stock_value.plot.bar()
plt.show()
