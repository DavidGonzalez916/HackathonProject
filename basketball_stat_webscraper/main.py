import time
import re
import selenium
import selenium.webdriver
import selenium.webdriver.chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select

from Locators import Locators
from sql_database.db import *
import pypyodbc as pyodbc
import pandas as pd 

class main:
  print("Do you want regular season stats? (y/n)")
  answer = input()
  if answer == "y":
    print("Which season do you want to see you can go as far back as 2001-02 season")
    season = input()
  else:
    print("Do you want postseason stats? (y/n)")
    answer = input()
    if answer == "y":
      print("Which season do you want to see you can go as far back as 2001-02 season")
      postseason = input()
  if answer == "n":
    print("Please Try Again")
    quit()

  driver = selenium.webdriver.Chrome()
  driver.get('https://www.espn.com/nba/stats')
  driver.implicitly_wait(5)

  locator = Locators(driver)
  locator.offensiveLeaders().click()
  count=1
  if season:
    dropdown = locator.season()
    dropdown.select_by_value(season + "|2")
  else:
    dropdown = locator.season()
    dropdown.select_by_value(postseason + "|3")
  time.sleep(1)
  table = locator.tableOfNames()
  for t in table:
    name = re.split(" |\n", t.text)
    try:
      if name[2] == "Jr.":
        team = name[3]
      else:
        team = name[2]
    except IndexError:
      total=0
      index=None
      for x, n in enumerate(name[1]):
        if n.isupper():
          if not total:
            index=x
          total+=1
        else:
          total=0
      team = name[1][index:total+(index)]
      name[1] = name[1].removesuffix(team)
    position = (driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[1]").text)
    ppg = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[4]").text)
    rpg = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[14]").text)
    ast = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[15]").text)

    params = (count, name[0], name[1], team, position, ppg, rpg, ast)
    cursor.execute("exec updatePlayers @id = ?, @firstName = ?, @lastName = ?, @team = ?, @position = ?, @ppg = ?, @rpg = ?,@apg = ?", params)

    if count == 50:
      break;
    count += 1

  cursor.execute("SELECT * FROM dbo.Players")
  cursor.fetchall()
  df = pd.read_sql_query("SELECT * FROM dbo.Players", db)
  print(df)

  db.commit()
  cursor.close()
  time.sleep(3)
  driver.quit()