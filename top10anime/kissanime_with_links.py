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

class Anime:
    title=""
    latest_ep=""
    previous_ep =""
    latest_ep_link=""
    
    def __init__(self):
        self.previous_ep = self.latest_ep

    def __str__(self):
        return self.title + ":\n" + self.latest_ep + "\n" + self.latest_ep_link + '\n'

anime = [Anime() for i in range(10)]

with open("top10_anime_kissanime_with_links.txt",'r') as file:
    c = file.read()

try:
    c = c.split('\n\n')

    for i in enumerate(c):
        temp = i[1].split('\n')[1]
        print(temp)
        anime[i[0]].previous_ep = temp
except:
    pass

for i in enumerate(elem):
    if(i[0]<10):
        anime[i[0]].title = i[1].find_all('a')[1].text
        anime[i[0]].latest_ep = i[1].find_all('p')[1].text.strip('Latest:\xa0')
        anime[i[0]].latest_ep_link = r'https://kissanime.ru/' + i[1].find_all('p')[1].find('a').get('href')

    
with open("top10_anime_kissanime_with_links.txt",'w') as file:
    for i in anime:
        print(i)
        try:
            file.write(i.title + ':\n' + i.latest_ep + '\n')
            if(i.previous_ep != i.latest_ep):
                file.write("UPDATED!!!\n")
            file.write(i.latest_ep_link + '\n\n')
        except:
            pass
br.quit()