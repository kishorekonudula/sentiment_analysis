from bs4 import BeautifulSoup
import bs4
import requests
import os
import time
import pandas as pd
from datetime import datetime as dt
import json
import pprint 



def scrape_reviews(page_url):
	page = requests.get(page_url, headers={'User-Agent': 'Mozilla/5.0'})
	if page.status_code == 200:
	    soup = BeautifulSoup(page.content, "html.parser")
	    glassdoor_reviews = {}
	    soup_find_all = soup.find_all('div', class_='hreview')
	    for review, soup_item in enumerate(soup_find_all):
	        for child in soup_item:
	            if child.findChild('time', class_="date subtle small"):
	                dt = child.findChild('time', class_="date subtle small").text
	                print("Date:", dt)
	            for ch in child:
	                if ch.findChild('span', class_="summary "):
	                    summary = ch.findChild('span', class_="summary ").text
	                    print("Summary:", summary)
	            for chch in ch:
	                if chch.findChild('p', class_=" pros mainText truncateThis wrapToggleStr"):
	                    pros = chch.findChild('p', class_=" pros mainText truncateThis wrapToggleStr").text
	                    print("Pros:", pros)
	                if chch.findChild('p', class_=" cons mainText truncateThis wrapToggleStr"):
	                    cons = chch.findChild('p', class_=" cons mainText truncateThis wrapToggleStr").text
	                    print("Cons:", cons)
	        print("----")
	        review_dict = {"Date": dt,
	                      "Summary": summary,
	                      "Pros": pros,
	                      "Cons": cons} 
	        glassdoor_reviews[review] = review_dict
	    return glassdoor_reviews
	else:
	    print("Request Failed")
    

#URLs:
for p in range(1, 11):
	glassdoor_url = "https://www.glassdoor.com/Reviews/McDonald-s-Reviews-E432_P{}.htm".format(p)
	reviews = scrape_reviews(glassdoor_url)
	with open('glassdoor_reviews{}.json'.format(p), 'w') as f:
		json.dump(reviews, f)
	time.sleep(1)
	


