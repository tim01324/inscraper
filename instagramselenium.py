from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
import time
import os
import wget

# edge browser
options = EdgeOptions()
options.use_chromium = True
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = Edge(options=options)

# for instagram
driver.get("https://www.instagram.com/")

# for username and password
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)

password = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "password"))
)

login = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')

# clear if there is a content in already
username.clear()
password.clear()

yourusername = ''
yourpassword = ''
username.send_keys(yourusername)
password.send_keys(yourpassword)
login.click()

search = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
)

# the stuff you are looking for
keyword = ''

search.send_keys(keyword)
time.sleep(1)
search.send_keys(Keys.RETURN)
time.sleep(2)
search.send_keys(Keys.RETURN)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'FFVAD'))
)

# file path
path = os.path.join(keyword)

# create file if not exists
if not os.path.exists(keyword):
    # path = os.path.join(keyword)
    os.mkdir(path)

# store all the srcs
srcs = []

## scroll by range
# for i in range(5):
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#     time.sleep(2)


# infinite scroll
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    # Get all img elements
    imgs = driver.find_elements_by_class_name('FFVAD')

    for img in imgs:
        if img.get_attribute('src') not in srcs:
            srcs.append(img.get_attribute('src'))

count = 0

for src in srcs:
    save_as = os.path.join(path, keyword + str(count) + '.jpg')
    wget.download(src, save_as)
    count += 1
