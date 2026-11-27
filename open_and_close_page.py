from selenium import webdriver
import data

driver = webdriver.Chrome()

driver.get(data.URBAN_ROUTES_URL)

assert "tripleten-services.com" in driver.current_url

driver.quit()