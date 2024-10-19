import csv
from pathlib import Path

root_dir = Path(__file__).parent

# interpret csv file

# compute each item into a hash
# hash Key is the "milestone point level"

# hash would be the nearest 500 point milestone

# store list of items at that hash

# value = 505

# key = value // 500


# print(key)

# item_hash = hash( key  )


# print( item_hash)

# print (hash(10001000//500))

points_table = {}

class Bonvoy_Item:
	def __init__(self, name, point_cost, url):
		self.name = name
		self.point_cost = point_cost
		self.url = url



# interpret csv

def read_csv(filename):
	with open(filename, mode='r') as file:
		csvFile = csv.reader(file)

		next(file) #skip first line
		for lines in csvFile:
			# read line
			csv_name = lines[0]
			csv_cost = lines[1]
			csv_url = lines[2]
			# print(csv_name, csv_cost, csv_url)
			item = Bonvoy_Item(csv_name, csv_cost, csv_url)
			
			item_hash = simple_hash(csv_cost)

			if item_hash not in  points_table:
				# put it in the table
				items = [item]
				points_table[item_hash] = items
			else:
				#append item to existing list
				points_table[item_hash].append(item)

			# print(item)
			# print(lines)

def ask_about(curr_points):
	curr_hash = simple_hash(curr_points)

	#check if it doesnt exist

	if curr_hash not in points_table:
		# print("test")
		# recompute hash to 500 points lower
		ask_about(curr_points - 500)
	else:
		items_list = points_table[curr_hash]

		print("There are " + str(len(items_list)) + " item(s) you can redeem now!")
		for item in items_list:
			print(item.name, item.point_cost)

def simple_hash(cost):
	hash = int(cost) // 500
	return hash


input_csv = 'BonvoyShopItems.csv'
full_path_of_csv = root_dir / input_csv
read_csv(full_path_of_csv)

# print(points_table)

current_points = 1000000
ask_about(current_points)




