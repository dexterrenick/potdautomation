#!/usr/bin/env python3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import praw
import smtplib
import time



def getPOTDLink():
    """
    Given POTD filtered page, sends most recent POTD
    """
    link = "https://www.reddit.com/r/sportsbook/?f=flair_name%3A%22POTD%22"
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver.delete_all_cookies()
    driver.get(link)
    driver.find_element_by_xpath('//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[4]/div[2]').click()
    url = driver.current_url;
    driver.quit()
    return(url);

def getTopLevelReplies():
    """
    Gets the top 5 POTD's from thread
    """
    list = []
    link = reddit.submission(url=getPOTDLink())
    link.comments.replace_more(limit=0)
    for top_level_comment in link.comments:
        #fix cleanup pick link
        list.append(top_level_comment.body);
    cleanList = [i for i in list if i]
    return list[1:13]

def getPickLine(comment):
    """
    Gets the actual pick rather than the entire write up
    """
    for line in comment.splitlines():
        if 'pick' in line.lower(): #and not('last' in line.lower()) and not('previous' in line.lower()) and not('overall' in line.lower()):
            return line;

def sendtext(messege):
    f = open("google_password.txt", "r")
    password = f.read()
    f.close()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("dexter.renick@gmail.com", password)
    server.sendmail("dexter.renick@gmail.com", "6268086588@vtext.com", messege)
    server.quit()


reddit = praw.Reddit(client_id='4sqxiXtPXVQsLg', client_secret='VaQpWp1ar05hTnszsTBXW9sH_DIzhg', user_agent='POTD_Scraper')
picks = getTopLevelReplies()

for x in range(len(picks) - 1):
    f = open(str(x+1) + "POTD.txt","w+")
    f.write(picks[x])

    #sendtext(pick)
