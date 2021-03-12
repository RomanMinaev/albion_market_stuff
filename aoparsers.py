import requests
import json


def JSON_items_pull():
	html_data = requests.get(
		'https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json')
	json_data = html_data.json()
	with open('items.json', 'w', encoding='utf8') as file:
		json.dump(json_data, file, indent=4, ensure_ascii=False)
