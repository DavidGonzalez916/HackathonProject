import time
import selenium
import selenium.webdriver
import selenium.webdriver.chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Locators import Locators

class main:

  driver = selenium.webdriver.Chrome()
  driver.get('https://www.basketball-reference.com/')
  driver.maximize_window()

  locator = Locators(driver)
  locator.search().send_keys("PPG" + Keys.ENTER )
  table = locator.tableOfNames()
  for t in table:
    print(t.text)

  time.sleep(3)
  driver.quit()