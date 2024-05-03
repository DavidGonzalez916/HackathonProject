from selenium.webdriver.common.by import By

class Locators:

  def __init__(self, driver):
    self.driver = driver
  
  searchBar = (By.CSS_SELECTOR, ".ac-input.completely")
  table = (By.XPATH, "(//table[@id='tot'])//a")

  pts = (By.XPATH, "//div[@class='p1']//div[2]/p[2]")
  trb = (By.XPATH, "//div[@class='p1']//div[3]/p[2]")
  ast = (By.XPATH, "//div[@class='p1']//div[4]/p[2]")

  def search(self):
    return self.driver.find_element(*Locators.searchBar)
  
  def tableOfNames(self):

    return self.driver.find_elements(*Locators.table)
  
  def points(self):
    return self.driver.find_element(*Locators.pts)
  
  def rebounds(self):
    return self.driver.find_element(*Locators.trb)
  
  def assists(self):
    return self.driver.find_element(*Locators.ast)

