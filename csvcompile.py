#!/usr/bin/env python3
# Uses the fetcher script and
# makes a folder of CSV files
# with it.
#
# Made by @Severnarch

import fetcher
import os

print(f"Fetching all items...")
icode, items, iend = fetcher.fetch_items()
if icode != 200:
	print(f" -> Failed with error code {icode}")
if not os.path.isdir("sheets"):
	os.mkdir("sheets")
parseItems = []
for cat in items.keys():
	for item in items[cat]:
		print(f"Fetching prices for item '{item[0]}'")
		pcode, prices = fetcher.fetch_prices(item[1])
		highPrice,lowPrice,avgPrice = 0,0,0
		if pcode == 200 and prices != []:
			# TODO: Remove anomalies in prices (e.g. stupidly overpriced listings)
			highPrice = max(prices)
			lowPrice = min(prices)
			avgPrice = round(sum(prices)/len(prices))
			print(f" -> High {highPrice}, Low {lowPrice}, Avg {avgPrice}")
		else:
			if pcode != 200:
				print(f" -> Failed with error code {pcode}")
			else:
				print(f" -> None for sale")
		parseItems.append([item[0],cat,item[1],highPrice,lowPrice,avgPrice,len(prices)])
with open("sheets/items.csv","w",encoding="utf-8",newline="\r\n") as f:
	f.write("name,category,id,highPrice,lowPrice,avgPrice,priceResults\n")
	for item in parseItems:
		f.write(",".join([str(x) for x in item])+"\n")