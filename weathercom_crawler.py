from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

t = time.time()
driver = webdriver.Firefox()

try:
  driver.get('https://weather.com/weather/hourbyhour/l/90272:4:US')
  print 'got website'

  elem = driver.find_element_by_class_name('ls-display-btn')
  print 'found button'

  elem.click()
  print 'clicked'

  elems = driver.find_elements_by_tag_name('tr')

  weathers = []
  for elem in elems:
    weathers.append(elem.find_elements_by_css_selector('*'))

  parsed_weathers = []

  for weather in weathers:
    tmp_list = []
    for el in weather:
      if el.tag_name == 'td':
        tmp_list.append(el.text)
    parsed_weathers.append(tmp_list)
  
  for x in parsed_weathers:
    print x


finally: 
  print int(time.time() - t)
  driver.close()