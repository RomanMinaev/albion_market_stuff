import requests
import json
import re
from json import JSONDecodeError
from random import randint


# https://render.albiononline.com/v1/item/ for item pics
class AOParsers:
	def __init__(self):
		return

	@staticmethod
	def JSON_items_pull():
		html_data = requests.get(
			'https://raw.githubusercontent.com/broderickhyman/ao-bin-dumps/master/formatted/items.json')
		json_data = html_data.json()
		with open('items.json', 'w', encoding='utf8') as file:
			json.dump(json_data, file, indent=4, ensure_ascii=False)

	@staticmethod
	def JSON_price_pull(itemId, quality):
		if '@' in itemId:
			fixed_itemId = itemId.replace('@', '%40')
			# print('AOParsers: Fixed @ symbol')
		else:
			fixed_itemId = itemId
		html_data = requests.get(
			f'https://www.albion-online-data.com/api/v2/stats/Prices/{fixed_itemId}.JSON?qualities={quality}', timeout=5)
		json_data = html_data.json()
		# print('AOParsers: json_data was parsed')
		with open('respond.json', 'w') as file:
			json.dump(json_data, file, indent=4)

	@staticmethod
	def JSON_price_get():
		arthurs_rest = []
		morgana_rest = []
		merlyns_rest = []
		black_market = []
		caerleon = []
		thetford = []
		fort_sterling = []
		lymhurst = []
		bridgewatch = []
		martlock = []
		output = {
			'arthurs_rest': arthurs_rest, 'morgana_rest': morgana_rest,
			'merlyns_rest': merlyns_rest, 'black_market': black_market,
			'caerleon': caerleon, 'thetford': thetford,
			'fort_sterling': fort_sterling, 'lymhurst': lymhurst,
			'bridgewatch': bridgewatch, 'martlock': martlock}
		with open('respond.json', 'r') as file:
			respond = json.load(file)
			for count in range(len(respond)):
				one_pool = respond[count]
				if 'Arthurs Rest' in one_pool.values():
					arthurs_rest.append(respond[count])
				if 'Morgana Rest' in one_pool.values():
					morgana_rest.append(respond[count])
				if 'Merlyns Rest' in one_pool.values():
					merlyns_rest.append(respond[count])
				if 'Black Market' in one_pool.values():
					black_market.append(respond[count])
				if 'Caerleon' in one_pool.values():
					caerleon.append(respond[count])
				if 'Thetford' in one_pool.values():
					thetford.append(respond[count])
				if 'Fort Sterling' in one_pool.values():
					fort_sterling.append(respond[count])
				if 'Lymhurst' in one_pool.values():
					lymhurst.append(respond[count])
				if 'Bridgewatch' in one_pool.values():
					bridgewatch.append(respond[count])
				if 'Martlock' in one_pool.values():
					martlock.append(respond[count])
		return output

	@staticmethod
	def JSON_items_black_market_pull():
		count = 1
		list_to_JSON = []
		with open('black_market_items.json', 'w', encoding='utf8') as file_2:
			with open('items.json', 'r', encoding='utf8') as file:
				items_raw = json.load(file)
				for item in items_raw[1200:]:
					if item is None:
						continue
					unique_name = item['UniqueName']
					if '@3' not in unique_name:
						continue
					unique_name = re.findall('.+(?=@)', unique_name)[0]
					print(unique_name)
					print(count)
					count = count+1
					# try:
						# AOParsers.JSON_price_pull(unique_name, 1)
					# except JSONDecodeError:
						# continue
					# output_raw = AOParsers.JSON_price_get()['black_market']
					# output = output_raw[0]
					# sell_price_min_date = output['sell_price_min_date']  # 0001-01-01T00:00:00
					# sell_price_max_date = output['sell_price_max_date']
					# buy_price_min_date = output['buy_price_min_date']
					# buy_price_max_date = output['buy_price_max_date']
					# b = '0001-01-01T00:00:00'
					# if buy_price_min_date != b and buy_price_max_date != b:
					print(f'Added {item} in input list')
					list_to_JSON.append(item)
			json.dump(list_to_JSON, file_2, indent=4, ensure_ascii=False)

	@staticmethod
	def item_to_itemid(item_name):
		print(f'AOParsers: Finding Item ID of {item_name}.')
		with open('items.json', 'r', encoding='utf8') as file:
			items_raw = json.load(file)
			for item in items_raw:
				if item is None:
					continue
				localized_names = item['LocalizedNames']
				if localized_names is None:
					continue
				if item_name in list(localized_names.values()):
					itemId_with_points = item['UniqueName']
					if '@' in itemId_with_points:
						itemId = itemId_with_points[:-2]
					else:
						itemId = itemId_with_points

		return itemId

	@staticmethod
	def prices_sort(prices):
		return

	@staticmethod
	def black_market_flip(itemId, quality):
		# print(f'AOParsers: Pulling Black Market and Caerleon prices')
		AOParsers.JSON_price_pull(itemId, quality)
		prices = AOParsers.JSON_price_get()
		# print(prices)
		bm_prices = prices['black_market'][0]
		bm_price = bm_prices['buy_price_max']
		bm_date = bm_prices['buy_price_max_date']
		caerleon_prices = prices['caerleon'][0]
		caerleon_price = caerleon_prices['sell_price_min']
		caerleon_date = caerleon_prices['sell_price_min_date']
		potential_profit_taxed = float(bm_price) * float(0.97) - float(caerleon_price)
		rounded_profit = round(potential_profit_taxed)
		output = {
			'bm_price': bm_price, 'bm_date': bm_date,
			'caerleon_price': caerleon_price, 'caerleon_date': caerleon_date,
			'profit': rounded_profit, 'itemId': itemId, 'quality': quality}
		return output

	@staticmethod
	def get_rich():
		enchants = [0, 1, 2, 3]
		qualities = [1, 2, 3, 4, 5]
		quality_names = {1: 'Normal', 2: 'Good', 3: 'Outstanding', 4: 'Excellent', 5: 'Masterpiece'}
		with open('black_market_items.json', 'r', encoding='utf8') as file:
			items_raw = json.load(file)
			random_index = randint(0, len(items_raw) - 1)
			item = items_raw[random_index]
			unique_name = item['UniqueName']
			if '@' in unique_name:
				unique_name = re.findall('.+(?=@)', unique_name)[0]
			for enchant in enchants:
				if enchant == 0:
					continue
				else:
					unique_name = unique_name + f'@{enchant}'
				for quality_count in qualities:
					try:
						price = AOParsers.black_market_flip(unique_name, quality_count)
						print(price)
					except JSONDecodeError:
						continue
					if price['bm_date'] == '0001-01-01T00:00:00':
						return
					if price['profit'] > 10000:
						bm_price = price['bm_price']
						bm_date = price['bm_date']
						caerleon_price = price['caerleon_price']
						caerleon_date = price['caerleon_date']
						profit = price['profit']
						if caerleon_date != '0001-01-01T00:00:00':
							# output here
							output = {
								'bm_price': bm_price, 'bm_date': bm_date,
								'caerleon_price': caerleon_price, 'caerleon_date': caerleon_date,
								'profit': profit, 'itemId': unique_name, 'quality': quality_count}
							print(unique_name, quality_names[quality_count])
							print(
								f'**Item ID:** {unique_name}\n'
								f'**Black Market:** {bm_price}'
								f'**Last seen at:** {bm_date}\n'
								f'**Caerleon:** {caerleon_price} '
								f'**Last seen at:** {caerleon_date}\n'
								f'**Flip profit:** {profit}')
							print(output['itemId'])
							return output
						else:
							output = {
								'bm_price': 'None', 'bm_date': 'None',
								'caerleon_price': 'None', 'caerleon_date': 'None',
								'profit': 'None', 'itemId': None, 'quality': 'None'}
							return output

				unique_name = re.findall('.+(?=@)', unique_name)[0]

