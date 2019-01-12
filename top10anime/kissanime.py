from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs


CHROME_PATH = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = r'C:\Users\141\AppData\Local\Programs\Python\Python37\chromedriver.exe'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

br = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          options=chrome_options
                         )  

br.get("https://kissanime.ru")
time.sleep(7)

try:
    myElem = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.ID, 'tab-trending')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading took too much time!")

ps = br.page_source

soup = bs(ps,"html.parser")

elem = soup.find_all("div",{"style":"position:relative"})
temp = []

for i in elem:
    temp.append(i.find_all('a')[1].text)

top10 = []
for i in range(10):
    top10.append(temp[i])
    
with open("top10_anime_kissanime.txt",'w') as file:
    for i in top10:
    	print(i)
    	try:
    		file.write(i+'\n')
    	except:
    		pass
br.quit()