from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import accountInfoGenerator as account
import getVerifCode as verifiCode
import fakeMail as email
import time
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver

PROXY_LIST = [
'138.128.32.25:8800',
'154.9.41.195:8800',
'154.9.41.222:8800',
'212.115.61.163:8800',
'5.253.117.98:8800',
'212.115.61.64:8800',
'138.128.32.71:8800',
'138.128.32.173:8800',
'138.128.32.226:8800',
'5.253.117.254:8800'
]

parser = argparse.ArgumentParser()
args = parser.parse_args()
ua = UserAgent()
userAgent = ua.random

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")
chrome_options.add_argument(f'user-agent={userAgent}')
chrome_options.add_argument('--proxy-server=23.250.40.33:8800')
# chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(r'/Users/victoryip/instagram-auto-create-account-master/chromedriver', options=chrome_options)

# driver.get("https://nordvpn.com/zh-tw/what-is-my-ip/")

#saves the login & pass into accounts.txt file.
acc = open("accounts.txt", "a")

driver.get("https://10minutemail.net/")

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


# print(soup.find_all("span", {"id": "span_mail"})[0].text)

# mail = soup.find_all("span", {"id": "span_mail"}).text

mail = soup.find_all("input", {"id": "fe_text"})[0]['value']

verifiCodeInMail = ''

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get("https://www.instagram.com/accounts/emailsignup/")

time.sleep(2)
try:
    cookie = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,
                                                                         '/html/body/div[3]/div/div/button[1]'))).click()
except:
	pass
name = account.username()

#Fill the email value
email_field = driver.find_element_by_name('emailOrPhone')
fake_email = mail
email_field.send_keys(fake_email)
print(fake_email)

# Fill the fullname value
fullname_field = driver.find_element_by_name('fullName')
fullname_field.send_keys(account.generatingName())
print(account.generatingName())

# Fill username value
username_field = driver.find_element_by_name('username')
username_field.send_keys(name)
print(name)

# Fill password value
password_field = driver.find_element_by_name('password')
acc_password = account.generatePassword()
password_field.send_keys(acc_password) # You can determine another password here.

print(name+":"+acc_password, file=acc)

acc.close()

time.sleep(3)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/form/div[7]/div/button"))).click()

time.sleep(8)

#Birthday verification
driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select/option[4]"))).click()

driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select/option[10]"))).click()

driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select").click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select/option[27]"))).click()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[6]/button"))).click()
time.sleep(3)

driver.switch_to.window(driver.window_handles[0])

checking = True

while checking:
    driver.refresh()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    for i in soup.find_all("a"):
       if "is your Instagram code" in i.text:
           driver.switch_to.window(driver.window_handles[1])
           verifiCodeInMail = i.text.split()[0]
           checking = False
           break;

    time.sleep(5)

time.sleep(2)

driver.find_element_by_name('email_confirmation_code').send_keys(verifiCodeInMail, Keys.ENTER)

time.sleep(2)

# time.sleep(8)

#805912