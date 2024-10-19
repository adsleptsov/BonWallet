import csv
import json
from pathlib import Path

root_dir = Path(__file__).parent

def make_json (csv_filename, json_filename):
	data = []

	with open(csv_filename, encoding="utf-8", mode='r') as csv_file:
		csvreader = csv.DictReader(csv_file)

		# next(csv)

		for rows in csvreader:
			data.append(rows)

	with open(json_filename, mode='w', encoding='utf-8') as json_file:
		json_file.write(json.dumps(data, indent=4))


csvFilePath = root_dir / 'BonvoyShopItems.csv'
jsonFilePath = root_dir / 'BonvoyShopJSON.json'

make_json(csvFilePath, jsonFilePath)