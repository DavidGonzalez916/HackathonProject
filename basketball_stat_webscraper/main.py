import time
import selenium
import selenium.webdriver
import selenium.webdriver.chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Locators import Locators
from sql_database.db import *
import pypyodbc as pyodbc

class main:

  driver = selenium.webdriver.Chrome()
  driver.get('https://www.basketball-reference.com/')
  driver.maximize_window()

  locator = Locators(driver)
  locator.search().send_keys("PPG" + Keys.ENTER )
  count=1
  table = locator.tableOfNames()
  for t in table:
    name = (t.text).split(' ')
    params = (name[0], name[1], count)
    cursor.execute("exec change_name @firstName = ?, @lastName = ?, @id = ?", params)
    if count == 75:
      break
    count+=1

  db.commit()

  time.sleep(3)
  driver.quit()