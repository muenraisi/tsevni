import akshare as ak
import common.print
import datetime
import pandas as pd

CORPORATE_BOND_LABEL = ['国债', '有担保企业债(AAA+)', '有担保企业债(AAA)', '企业债(AAA-)', '有担保企业债(AA+)', '有担保企业债(AA)', '有担保企业债(AA-)',
                        '无担保企业债(AAA(2))', '无担保企业债(AA+(2))', '无担保企业债(AA(2))', '无担保企业债(AA-(2))', '企业债(A+)', '企业债(A)',
                        '企业债(A-)', '企业债(BBB+)',
                        '企业债(BBB)', '企业债(BB)', '企业债(B)']


def get_all_corporate_bond_rate():
    today=datetime.datetime.today()
    trade_date = list(ak.tool_trade_date_hist_sina()["trade_date"])
    # print(trade_date)
    while today.strftime("%Y-%m-%d") not in trade_date:
        today = today - datetime.timedelta(days=1)
    last_trade_day = today.strftime("%Y-%m-%d")
    # print(last_trade_day)
    dfs=[]
    for label in CORPORATE_BOND_LABEL:
        bond_rate = ak.bond_china_close_return(symbol=label, start_date=last_trade_day, end_date=last_trade_day)
        bond_rate.set_index("期限",inplace=True)
        bond_rate.drop(columns=['日期','到期收益率','远期收益率'],inplace=True)
        bond_rate.rename(columns={"即期收益率": label}, inplace=True)
        dfs.append( bond_rate)
    res = pd.concat(dfs, join='outer', axis=1)
    return res


def get_map_bond(issuer_rating_cd, guarantor=""):
    if issuer_rating_cd in ['A+', 'A', 'A-', 'BBB+', 'BBB', 'BB', 'B']:
        return '企业债(' + issuer_rating_cd + ')'
    else:
        if guarantor != "":
            return '有担保企业债(' + issuer_rating_cd + ')'
        else:
            return '无担保企业债(' + issuer_rating_cd + '(2))'


'''
    bond_id   bond_nm  stock_id  stock_nm btype convert_price convert_price_valid_from  convert_dt maturity_dt 
    债券代码  债券名称  股票代码    股票名称 购买者    转股价         （生效日期？）         转股起始日   债券到期日   
    127003  海印转债  sz000861  海印股份     C          3.00               2020-07-17  2016-12-16  2022-06-08     

    next_put_dt put_dt          put_notes           put_price   put_inc_cpn_fl  put_convert_price_ratio  put_count_days    
    回售起始日 （回售日期都是None）回售消息(都是None）   回售价格   (回售？）        (回售时股价/当前股价）     回售触发天数
    2020-06-08   None            None               100.000     y               94.59                    30              

    put_total_days  put_real_days repo_discount_rt repo_valid_from repo_valid_to turnover_rt  
    回售总天数        实际回售天数     （？？？）        （？？？）       （？？？）   当日换手率（%）
    30              0             0.00            None          None        1.18
    
    redeem_price redeem_inc_cpn_fl redeem_price_ratio  redeem_count_days  redeem_total_days  redeem_real_days redeem_dt 
    到期赎回价       （？？？）      (强赎条件价/转股价%）     强赎触发天数          强赎总天数       实际强赎天数     强赎日期    
      110.000           n            130.000                 15                 30                 0      None              

    redeem_flag                             orig_iss_amt curr_iss_amt  
    赎回标志(Y:赎回， X:未满足， N:不赎回）    发行规模（亿） 剩余规模（亿）
    X                                       11.110        6.738
    
    
    rating_cd issuer_rating_cd      guarantor                         ssc_dt esc_dt sc_notes market_cd force_redeem 
    主体评级    债券评级              担保方                            ？？   ??        ??      市场?     强制赎回
        AA     AA                   广州海印实业集团有限公司责任人担保   None   None     None      szmb         None                    
        
    real_force_redeem_price convert_cd repo_cd     
    实际赎回价格              转债代码    ？？代码
    None                    127003    None

     ration ration_cd apply_cd online_offline_ratio qflag qflag2 ration_rt  fund_rt margin_flg lt_bps    pb pb_flag  
    配售比例    配售代码 申购代码   线上线下比例          ？   ？    股东配售率  ？？        ？？       ??   市净  跌破市净
    0.4938    080861   070861                    4     N      N      None     buy          R      ""    1.27       N     

    total_shares  float_shares sqflg sprice  \
    总股本           流通股      ??     股价
    2325501918.0  2167749455.0     Y   2.22

     svolume sincrease_rt qstatus bond_value bond_value2 volatility_rate last_time    convert_value premium_rt year_left 
     成交额    股票涨跌比      ？？       ？？      ？？              ？？     最后时间       转股价值    转股溢价率  剩余期限
     6556.42    -1.77%      00        buy         buy             buy       15:00:03       74.00     37.58%     1.279     

    ytm_rt      ytm_rt_tax    price     full_price          increase_rt  volume     convert_price_valid    
    税前收益    税后收益        价格      价格（=price?)         涨跌比         成交量         能否转股？
    7.70%      5.88%          101.810    101.810                0.22%       810.85            Y

     adj_scnt      adj_cnt     redeem_icon     ref_yield_info  adjust_tip adjusted option_tip bond_value3 left_put_year
    成功下修次数    下修次数      回售？                ？？           ？？？       ？？      ？？      ？？          ？？
        2               2           -                   N            -         buy             - 

    short_maturity_dt   dblow   force_redeem_price   put_convert_price convert_amt_ratio    convert_amt_ratio2                          
        到期日             ??          ??                回售转股价       转债占流动市值比      转债占总市值比
          22-06-08      139.39               3.90         2.10             14.0%              13.1%  

            convert_amt_ratio_tips                  stock_net_value stock_cd pre_bond_id
        转债占比提示                                  ？？           股票代码     转债代码
    转债占流动市值比：14.0%\n转债占总市值比：13.1%     0.00     000861    sz127003  

    repo_valid               convert_cd_tip                         price_tips  
      赎回有效                    转股提示                             价格提示        
      有效期：-        127003；2016-12-16 开始转股           全价：101.810 最后更新：15:00:03  
'''

if __name__ == '__main__':
    print("")
    bond_convert_jsl_df = ak.bond_cov_jsl()

    # filter
    bond_convert_jsl_df = bond_convert_jsl_df[bond_convert_jsl_df["btype"] == "C"]  # 删除仅合格投资者可购买，这项为E
    # bond_convert_jsl_df.drop( ["btype", "convert_price_valid_from", "convert_dt", "next_put_dt", "put_dt",
    # "put_notes", "put_price"], axis=1, inplace=True)
    bond_convert_df = bond_convert_jsl_df[
        ["bond_nm", "rating_cd", "issuer_rating_cd", "ytm_rt", "ytm_rt_tax", "year_left", "premium_rt"]]
    bond_convert_df['ytm_rt'] = bond_convert_df['ytm_rt'].str.rstrip('%').replace('-', '-100', regex=False).astype(
        'float')
    bond_convert_df['ytm_rt_tax'] = bond_convert_df['ytm_rt_tax'].str.rstrip('%').replace('-', '-100',
                                                                                          regex=False).astype('float')
    bond_convert_df.sort_values(by=["ytm_rt_tax"], inplace=True, ascending=False)

    # print(bond_convert_df[bond_convert_df["bond_nm"]=="亚药转债"])
    # print(bond_convert_df.head(10))

    df_bond_rate = get_all_corporate_bond_rate()
    print(df_bond_rate)
    # for key, item in bond_rate_dict.items():
    #     print(key, item)
    df_bond_rate