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

# this url lists item by two parameters
#NrPP is likely something like number of item per page
#No= is the "starting item"

#i found that the max that can exist per page is 96 item


#so construct a loop that iterates through the theorized number of item
#right now it is 4289 numbers

#grab each item and put it into a csv file


#go to first page and calculate num of pages


total_num_of_items = 0


def generate_csv(init_url, file_name):
	starting_no = 0
	
	with open(file_name, 'w', encoding='utf-8', newline='') as csvfile:
		writecsv = csv.writer(csvfile, delimiter=',')

		writecsv.writerow(["Name of Item", "Item Point Value", "Item URL"])
		full_url = init_url+str(starting_no)

		print("Going to " + full_url)

		# shop_html = requests.get(full_url)

		shop_session = requests_html.HTMLSession()

		# go to the home page url first
		home_url = 'https://shop-with-points.marriott.com/15015MARNELITE'

		shop_html = shop_session.get(home_url)
		
		# print(shop_html.html.text)
		shop_html.html.render()
		
		
		# then go to the right url
		shop_html = shop_session.get(full_url)
		


		# print(shop_html.html.text)
		# soup = shop_html.html
		soup = BeautifulSoup(shop_html.html.raw_html, "lxml")
		# soup = BeautifulSoup(shop_html.html, "xml")
		# soup = BeautifulSoup(shop_html.content, "xml")
		total_num_of_items = 0

		if (starting_no == 0):
			# fetch total number of item
			total_num_of_items = int((soup.find(class_ = 'breadCrumbs').contents[0]).strip().split(" ")[0].split("(")[1])
			# print(total_num_of_items)

		
		num_of_pages = int(total_num_of_items / 96)

		# for i in range(num_of_pages):
		# 	# visit a page
		# 	# grab each item and store it in the csv
		
		# item = soup.find(id = 'itemsList')
		# item = soup.find_all(class_ = 'shortDescription')
		items = soup.find_all(class_ = 'shortDescription')

		# print(items.len())
		for item in items:
		
			# item = i
			item_name_and_url = item.findChild("a")
			# print(item_name_and_url)
			item_name = item_name_and_url.contents[0]
			item_url = "https://shop-with-points.marriott.com" + item_name_and_url['href']
			item_point_amount = int(item.findChild(class_ = "amount").contents[2].strip().replace(",",""))


			writecsv.writerow([item_name,item_point_amount,item_url])
			# print(item_name)
			# print(item_url)
			# print(item_point_amount)
		# print(item)



		
	
generate_csv(init_url,csv_name)



