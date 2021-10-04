from selenium import webdriver
from time import sleep
import iamarobot


driver = webdriver.Firefox()
driver.get('https://google.com/recaptcha/api2/demo')

sleep(4)
d = iamarobot.Docaptcha(driver, '//iframe[@title="reCAPTCHA"]')
d.solve()