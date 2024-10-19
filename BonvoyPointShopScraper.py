from bs4 import BeautifulSoup
# import requests
import csv
import os
import requests_html

# PYPPETEER_CHROMIUM_REVISION = '1263111'

# os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

# pip install requests_html
# pip install bs4
# pip install lxml_html_clean
# set pypeteer chromium revision to 1263111

init_url = 'https://shop-with-points.marriott.com/15015MARNELITE/search?Nrpp=96&No='

csv_name = 'BonvoyShopItems.csv'

# this url lists items by two parameters
#NrPP is likely something like number of items per page
#No= is the "starting item"

#i found that the max that can exist per page is 96 items


#so construct a loop that iterates through the theorized number of items
#right now it is 4289 numbers

#grab each item and put it into a csv file


#go to first page and calculate num of pages


total_items = 0


def generate_csv(init_url, file_name):
	starting_no = 0
	
	with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
		full_url = init_url+str(starting_no)

		print("Going to " + full_url)

		# shop_html = requests.get(full_url)

		shop_session = requests_html.HTMLSession()

		# go to the home page url first
		home_url = 'https://shop-with-points.marriott.com/15015MARNELITE'

		shop_html = shop_session.get(home_url)
		
		shop_html.html.render()
		# print(shop_html.html.text)
		
		
		# then go to the right url
		shop_html = shop_session.get(full_url)
		


		print(shop_html.html.text)

		# soup = BeautifulSoup(shop_html.content, "xml")

		# total_items = soup.find(class_ = 'breadCrumbs')
		# print(total_items)
		# if (starting_no == 0):
		# 	#fetch total number of items



		
	
generate_csv(init_url,csv_name)



