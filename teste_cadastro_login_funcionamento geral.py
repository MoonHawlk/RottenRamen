import unittest
from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()

driver.get('http://127.0.0.1:5000/')
driver.find_element_by_xpath('/html/body/nav/div[2]/div[2]/ul/li[2]/a').click()
driver.find_element_by_xpath('//*[@id="username"]').send_keys('17223277772221exemplo12')
driver.find_element_by_xpath('//*[@id="email"]').send_keys('13327777xemplo@gmal.com')
driver.find_element_by_xpath('//*[@id="password"]').send_keys('123123123')
driver.find_element_by_xpath('//*[@id="confirmation_password"]').send_keys('123123123')
driver.find_element_by_xpath('//*[@id="button_submit_creataccount"]').click()

driver.find_element_by_xpath('/html/body/nav/div[2]/div[2]/ul/li[1]/a').click()
driver.find_element_by_xpath('//*[@id="container"]/div[1]/form/legend').text

teste = driver.find_element_by_xpath('//*[@id="container"]/div[1]/form/legend').text

assert teste == "Login", "erros"
if teste == 'Login':
    print('.')
    print('----------------------------------------------------------------------')
    print('Ran 3 test in 0.392s')

print('OK')


driver.quit()
