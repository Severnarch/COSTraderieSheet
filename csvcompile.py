#!/usr/bin/env python3
# Uses the fetcher script and
# makes a folder of CSV files
# with it.
#
# Made by @Severnarch

import numpy as np
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
		fprices = []
		if pcode == 200 and prices != []:
			prices_array = np.array(prices)
			perc25 = np.percentile(prices_array, 25)
			perc75 = np.percentile(prices_array, 75)
			inteqr = perc75 - perc25
			lowbnd = perc25 - 1.5 * inteqr
			uppbnd = perc75 + 1.5 * inteqr
			fprices = [price for price in prices if lowbnd <= price <= uppbnd]
			print("     -> Prices: ",prices)
			print("     -> FPrices:",fprices)

			highPrice = max(fprices)
			lowPrice = min(fprices)
			avgPrice = round(sum(fprices)/len(fprices))
			print(f" -> High {highPrice}, Low {lowPrice}, Avg {avgPrice}")
		else:
			if pcode != 200:
				print(f" -> Failed with error code {pcode}")
			else:
				print(f" -> No listings met criteria")
		parseItems.append([item[0],cat,item[1],highPrice,lowPrice,avgPrice,len(prices),len(fprices)])
with open("sheets/items.csv","w",encoding="utf-8",newline="\r\n") as f:
	f.write("name,category,id,highPrice,lowPrice,avgPrice,rawPricesCount,filterPricesCount\n")
	for item in parseItems:
		f.write(",".join([str(x) for x in item])+"\n")