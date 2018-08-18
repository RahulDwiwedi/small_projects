import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")


from multiprocessing import Pool

url = "http://www.artculturefestival.in"


for i in range(10):

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1250, 820)
    driver.get(url)
    time.sleep(50)
    driver.find_element_by_id('menu-item-382').click()
    time.sleep(52)
    driver.find_element_by_css_selector('#menu-item-1438').click()
    time.sleep(150)
    driver.find_element_by_css_selector('#menu-item-381').click()
    time.sleep(50)
    print(i)
    driver.close()

# c = {"driver1": 'webdriver.Chrome(chrome_options=chrome_options)', "driver2": 'webdriver.Chrome(chrome_options=chrome_options)'}
#
# for k,v in c.items():
#     exec("%s=%s" % (k,v))
#     exec("%s.get('%s')" % (k, url))
#     time.sleep(20)


