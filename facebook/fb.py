from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.facebook.com/")


page = "Your FB Page Url"

f=open("fb_list.txt","r")
data = f.read().split("\n")


for d in data:
    email = d.split(" ")[0]
    psw = d.split(" ")[1]
    time.sleep(1)

    driver.find_element_by_css_selector("#email").clear()
    driver.find_element_by_css_selector("#email").send_keys(email)

    time.sleep(1)
    driver.find_element_by_css_selector("#pass").send_keys(psw)
    time.sleep(1)
    driver.find_element_by_css_selector("#loginbutton").click()
    print("getting in .........with " + email)
