from selenium.webdriver.common.by import By

class Locators:

  def __init__(self, driver):
    self.driver = driver
  
  searchBar = (By.CSS_SELECTOR, ".ac-input.completely")
  table = (By.XPATH, "(//table[@id='tot'])//a")

  def search(self):
    return self.driver.find_element(*Locators.searchBar)
  
  def tableOfNames(self):
    return self.driver.find_elements(*Locators.table)