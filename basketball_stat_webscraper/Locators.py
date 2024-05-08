from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class Locators:

  def __init__(self, driver):
    self.driver = driver
  
  offense = (By.XPATH, "//a[@href='/nba/stats/player']")
  dropdownSelect = (By.XPATH, "(//div[@class='flex flex-wrap']/div/div/select)[1]")
  getNames = (By.XPATH, "//td/div")
 

  def offensiveLeaders(self):
    return self.driver.find_element(*Locators.offense)
  
  def tableOfNames(self):
    return self.driver.find_elements(*Locators. getNames)
  
  def season(self):
    return Select(self.driver.find_element(*Locators.dropdownSelect))
 
  