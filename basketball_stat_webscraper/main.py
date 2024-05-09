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
  season=None
  fg, threePoint, ft, stl, blk, to = (False,) *6
  if answer == "y":
    print("Which season do you want to see you can go as far back as 2001-02 season")
    season = input()
    print("Would you like to add any other stats? (y/n)")
    updateStats = input()
 
  else:
    print("Do you want postseason stats? (y/n)")
    answer = input()
    if answer == "y":
      print("Which season do you want to see you can go as far back as 2001 season")
      postseason = input()
      print("Would you like to add any other stats? (y/n)")
      updateStats = input()

  if updateStats == "y":
    print("Which stat would you like to add? (FG%, 3P%, FT%, STL, BLK, TO)")
    updateStats = input()
    if "FG%" in updateStats:
      fg=True
      cursor.execute("ALTER TABLE dbo.Players ADD FieldGoal FLOAT")
    if "3P%" in updateStats:
      threePoint=True
      cursor.execute("ALTER TABLE dbo.Players ADD ThreePoint FLOAT")
    if "FT%" in updateStats:
      ft=True
      cursor.execute("ALTER TABLE dbo.Players ADD FreeThrow FLOAT")
    if "STL" in updateStats:
      stl=True
      cursor.execute("ALTER TABLE dbo.Players ADD STL FLOAT")
    if "BLK" in updateStats:
      blk=True
      cursor.execute("ALTER TABLE dbo.Players ADD BLK FLOAT")
    if "TO" in updateStats:
      to=True
      cursor.execute("ALTER TABLE dbo.Players ADD Turnovers FLOAT")
    db.commit()

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

    if fg:
      fieldGoal = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[7]").text)
      cursor.execute("UPDATE dbo.Players SET FieldGoal = ? WHERE Id = ?", (fieldGoal, count))
    if threePoint:
      threePointPercentage = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[10]").text)
      cursor.execute("UPDATE dbo.Players SET ThreePoint = ? WHERE Id = ?", (threePointPercentage, count))
    if ft:
      freeThrow = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[13]").text)
      cursor.execute("UPDATE dbo.Players SET FreeThrow = ? WHERE Id = ?", (freeThrow, count))
    if stl:
      steals = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[16]").text)
      cursor.execute("UPDATE dbo.Players SET STL = ? WHERE Id = ?", (steals, count))
    if blk:
      blocks = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[17]").text)
      cursor.execute("UPDATE dbo.Players SET BLK = ? WHERE Id = ?", (blocks, count))
    if to:
      turnovers = float(driver.find_element(By.XPATH, "//div[@class='Table__ScrollerWrapper relative overflow-hidden']/div/table/tbody/tr[" + str(count) + "]/td[18]").text)
      cursor.execute("UPDATE dbo.Players SET Turnovers = ? WHERE Id = ?", (turnovers, count))


    if count == 50:
      break;
    count += 1




      

  cursor.execute("SELECT * FROM dbo.Players")
  cursor.fetchall()
  df = pd.read_sql_query("SELECT * FROM dbo.Players", db)
  print(df)
  db.commit()
  
  if fg:
    cursor.execute("ALTER TABLE dbo.Players DROP COLUMN FieldGoal")
  if threePoint:
    cursor.execute("ALTER TABLE dbo.Players DROP COLUMN ThreePoint")
  if ft:
    cursor.execute("ALTER TABLE dbo.Players DROP COLUMN FreeThrow")
  if stl:
    cursor.execute("ALTER TABLE dbo.Players DROP COLUMN STL")
  if blk:
    cursor.execute("ALTER TABLE dbo.Players DROP COLUMN BLK")
  if to:
    cursor.execute("ALTER TABLE dbo.Players DROP COLUMN Turnovers")
  db.commit()
  cursor.close()
  time.sleep(3)
  driver.quit()