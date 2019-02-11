from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import sqlite3
from win10toast import ToastNotifier
import anime_class


conn = sqlite3.connect("anime.db")
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Anime (title TEXT, latest_ep TEXT, latest_ep_link TEXT)
    ''')

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

#find all elements of the top 10 anime list
elem = soup.find_all("div",{"style":"position:relative"})
temp = []



#instantiate 10 instances of Anime Class
anime = [anime_class.Anime() for i in range(10)]
toast = ToastNotifier()

#fill up the empty Anime instnaces with information grabbed from the page like title, latest episode, latest episode link
for i in enumerate(elem):
    if(i[0]<10):
        anime[i[0]].title = i[1].find_all('a')[1].text
        anime[i[0]].latest_ep = i[1].find_all('p')[1].text.strip('Latest:\xa0')
        anime[i[0]].latest_ep_link = r'https://kissanime.ru/' + i[1].find_all('p')[1].find('a').get('href')
        #print(anime[i[0]])
        #check if anime has been updated or not
        #debugging
        #import pdb ; pdb.set_trace()
        #Select from db latest episode of current anime being scanned
        cur.execute('''SELECT latest_ep FROM Anime WHERE title=?''', (anime[i[0]].title,))
        previous_ep_tmp = cur.fetchone()
        print(previous_ep_tmp)
        if(previous_ep_tmp != None):
            # if count of episode of current episode is greater than selected anime from db, then update db and toast it Bro!
            if(int(anime[i[0]].latest_ep.split()[1]) > int(previous_ep_tmp[0].split()[1])):
                cur.execute('''UPDATE Anime SET latest_ep = ? WHERE title = ?''', (anime[i[0]].latest_ep, anime[i[0]].title,))
                print(anime[i[0]].title + " UPDATED!!!!")
                toast.show_toast("ANIME UPDATED!!", anime[i[0]].title + " UPDATED!!!!")
                
conn.commit()

#initial test version
with open("top10_anime_kissanime_with_links.txt",'w') as file:
    cur.execute('''SELECT * FROM Anime''')
    data = cur.fetchall()

    for i in enumerate(data):
        if(i[0]<10):
            file.write(i[1][0] + '\n' + i[1][1])
            if(anime[i[0]].updated):
                file.write("\nUPDATED!!!!\n")
                anime[i[0]].updated = False
            #print(i[1][2])
            try:
                file.write('\n'+i[1][2])
            except:
                pass
            file.write('\n\n')
cur.close()
br.quit()