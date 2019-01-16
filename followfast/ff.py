import sys
from telnetlib import EC

from selenium import webdriver
import time
import urllib.request
from urllib.request import Request,urlopen
from PIL import Image
import pytesseract
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome()
driver.get('http://followfast.com/login.php')

element = driver.find_element_by_name("captcha")
actions = ActionChains(driver)
actions.move_to_element(element).perform()


driver.save_screenshot("screenshot.png")
wait = ui.WebDriverWait(driver, 20)



from PIL import Image
from pytesseract import pytesseract


def crop(image_path, coords, saved_location):
    """
    @param image_path: The path to the image to edit
    @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    print(image_obj.size)
    cropped_image = image_obj.crop(coords)
    cropped_image.save(saved_location)
    return cropped_image


cropped_image=crop('screenshot.png', (400, 550, 540, 580), 'cropped.png')
print (cropped_image)
text = pytesseract.image_to_string(cropped_image)
while text=="":
    text = pytesseract.image_to_string(cropped_image)
text=text.replace('(', '').replace(')', '')
print("Captcha : "+text)

time.sleep(1)
driver.find_element_by_css_selector("#username").send_keys("your email")
time.sleep(1)
driver.find_element_by_css_selector("#pass").send_keys("password")
time.sleep(1)
driver.find_element_by_name("captcha").send_keys(text)
time.sleep(1)

# wait.until(lambda driver: driver.find_element_by_id('HintHits'))

driver.find_element_by_name("login").click()
print ("login test")

#

urls =['http://followfast.com/youtube.php']#,'http://followfast.com/reddit.php']
for url in urls:
    driver.get(url)
    time.sleep(1)
    for i in range(20):
        driver.find_element_by_css_selector(".submit").click()
        time.sleep(43)
        print(str(i+1)+" videos watched")


driver.close()
