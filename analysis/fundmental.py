import akshare as ak
import common.print


def core(stock_code):
    def clean(x):
        if x == "--":
            x = 0
        return float(x)

    df_profit = ak.stock_financial_profit_statement(stock=stock_code).applymap(clean)
    df = df_profit[[]]
    df["净利率"] = df_profit["五、净利润"] / df_profit["营业收入"]
    df["毛利率"] = (df_profit["营业收入"] - df_profit["营业成本"]) / df_profit["营业收入"]
    df_profit["EBIT"] = df_profit["五、净利润"] + df_profit["减：所得税费用"] + df_profit["财务费用"]
    df["经营利润率"] = df_profit["EBIT"] / df_profit["营业收入"]
    df["所得税率"] = df_profit["减：所得税费用"] / df_profit["四、利润总额"]
    df["经营税比"] = df_profit["营业税金及附加"] / df_profit["减：所得税费用"]
    df["利息负担"] = df_profit["财务费用"] / df_profit["EBIT"]
    df["总费率"] = (df_profit["销售费用"] + df_profit["管理费用"] + df_profit["财务费用"] + df_profit["研发费用"]) / df_profit["二、营业总成本"]
    df["销售费率"] = df_profit["销售费用"] / df_profit["二、营业总成本"]
    df["管理费率"] = df_profit["管理费用"] / df_profit["二、营业总成本"]
    df["财务费率"] = df_profit["财务费用"] / df_profit["二、营业总成本"]
    df["研发费率"] = df_profit["研发费用"] / df_profit["二、营业总成本"]
    return df


if __name__ == "__main__":
    #
    print(core("000488"))