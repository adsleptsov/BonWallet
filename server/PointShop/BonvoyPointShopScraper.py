from bs4 import BeautifulSoup, SoupStrainer
# import requests
import csv
import requests_html
import time


# pip install requests_html
# pip install bs4
# pip install lxml_html_clean
# set pypeteer chromium revision to 1263111

init_url = 'https://shop-with-points.marriott.com/15015MARNELITE/search?Nrpp=96&Ns=sku.nowPaxPrice|0&No='

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
	start_time = time.time()
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
		
		for i in range(num_of_pages+1):
		# for i in range(3):

			start_time_of_page = time.time()

			print("Scraping page: " + str(i))

			new_item_no = (i*96)
			page_of_items = []
			#could be 96 or 97 pages
			# new_item_no = 336
			
			full_url = init_url + str(new_item_no)
			shop_html = shop_session.get(full_url)

			strainer = SoupStrainer("li", attrs={"class": "shortDescription"})

			soup = BeautifulSoup(shop_html.html.raw_html, "lxml", parse_only=strainer)


			# soup.renderContents
			# print(soup.contents)

			# items = soup.find_all(class_ = 'shortDescription')
			items = soup.select('.shortDescription')


			# print(items.len())
			for item in items:
				# print(item)
				# item = i
				# item_name_and_url = item.findChild("a")
				item_name_and_url = item.select_one("a")
				# print (item_name_and_url.get_text())

				# print(item_name_and_url)
				# item_name = item_name_and_url.contents[0].replace('"','')
				item_name = item_name_and_url.get_text().replace('"',"")
				item_url = "https://shop-with-points.marriott.com" + item_name_and_url['href']

				# print(item.select_one(".amount").get_text().strip().strip(','))
				# item_amount = item.findChild(class_ = "amount").get_text().strip().replace(",","")
				item_amount = item.select_one(".amount").get_text().strip().replace(',','')
				# if item_amount.findChild("span"):
				# 	# print(item_amount.contents[4])
				# 	item_point_amount = int(item_amount.contents[4].strip().replace(",",""))
				# else:
				# 	item_point_amount = int(item.findChild(class_ = "amount").contents[2].strip().replace(",",""))

				# print(item_amount)

				if "Starting" in item_amount:
					item_amount = item_amount.split("\n")[2].strip()
					# print(item_amount)

				page_of_items.append([item_name,item_amount,item_url])
				# writecsv.writerow([item_name,item_amount,item_url])
				# print(item_name)
				# print(item_url)
				# print(item_point_amount)
			
			writecsv.writerows(page_of_items)
			end_time_of_page = time.time()
			print("page scrap time: ", end_time_of_page - start_time_of_page)
			# print(item)
	end_time = time.time()

	print("Total exec time: ", end_time - start_time)


		
	
generate_csv(init_url,csv_name)



