from selenium import webdriver
import selenium.webdriver.support.ui as ui
browser = webdriver.Chrome()
# 当测试好能够顺利爬取后，为加快爬取速度可设置无头模式，即不弹出浏览器
# 添加无头headlesss 1使用chrome headless,2使用PhantomJS
# 使用 PhantomJS 会警告高不建议使用phantomjs，建议chrome headless
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(chrome_options=chrome_options)
# browser = webdriver.PhantomJS()
# browser.maximize_window()  # 最大化窗口,可以选择设置

wait = ui.WebDriverWait(browser, 10)
browser.get('http://emweb.securities.eastmoney.com/PC_HKF10/FinancialAnalysis/index?type=web&code=01812&color=b')

wait.until(lambda driver: driver.find_element_by_id("tlp_data"))
element = browser.find_element_by_id('tlp_data')  # 定位表格，element是WebElement类型
# 提取表格内容td
# wait.unit(lambda element: element.find_elements_by_tag_name("td"))
print(element.text)
td_content = element.find_elements_by_tag_name("td") # 进一步定位到表格内容所在的td节点
lst = []  # 存储为list
for td in td_content:
    lst.append(td.text)
print(lst) # 输出表格内容