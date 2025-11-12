#!/usr/bin/env python3
# Fetches data from Traderie
# and returns it as JSON
# objects.
#
# Made by @Severnarch

import cloudscraper
import time

RESULTS_PER_PAGE = 50
REQUESTS_PER_MINUTE = 80
BLACKLISTED_PROPERTIES = [
	"stored","plushies 1","plushies 2","gender","venerated" #Generic
	"weight","bite","max stamina","speed","health","damage" #Traits
]

def get_scraper():
	scraper = cloudscraper.create_scraper()
	scraper.headers.update({
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Connection":"keep-alive",
		"User-Agent":"Mozilla/5.0 Gecko/20100101 Firefox/144.0",
	})
	return scraper

def fetch_tags():
	tagsUrl = "https://traderie.com/api/creaturesofsonaria/tags/items"
	scraper = get_scraper()
	request = scraper.get(tagsUrl)

	content = {}
	if request.status_code == 200:
		response = request.json()
		categories = list(response["tags"].keys())
		tags = {}
		for cat in categories:
			tags[cat.lower()] = [tag["tag"] for tag in response["tags"][cat]]
		content = tags

	return request.status_code, content

def fetch_items():
	itemsUrl = "https://traderie.com/api/creaturesofsonaria/items?page="
	scraper = get_scraper()

	endReached = False
	page = 0
	items = {}

	while not endReached:
		print(f" -> Fetching items page {page}")
		request = scraper.get(itemsUrl+str(page))

		if request.status_code == 200:
			response = request.json()
			resitems = list(response["items"])
			if len(resitems) != 0:
				iitem = 0
				while iitem < len(resitems):
					item = resitems[iitem]
					iitem += 1
					if not item["type"].lower() in items.keys():
						items[item["type"].lower()] = []
					if item["active"]:
						items[item["type"].lower()].append([item["name"], item["id"]])
			else:
				endReached = True
				status = 200
		else:
			status = request.status_code
			break

		page += 1

	return status, items, endReached

def fetch_prices(item):
	listingsUrl = "https://traderie.com/api/creaturesofsonaria/listings?itemTags=true&makeOffer=false&selling=true&auction=false&item="
	scraper = get_scraper()

	endReached = False
	page = 0
	prices = []

	earlyReqMin = 0
	reqsDone = 0
	status = 0

	while not endReached:
		print(f" -> Fetching listings page {page}")
		request = scraper.get(listingsUrl+str(item)+"&page="+str(page))
		elapse = time.time()-earlyReqMin
		if elapse >= 60:
			earlyReqMin = time.time()
			elapse = 0
			reqsDone = 0
		reqsDone += 1

		if request.status_code == 200:
			response = request.json()
			reslists = list(response["listings"])
			if reslists == []:
				endReached = True
				break
			if len(reslists) != 0:
				ilist = 0
				while ilist < len(reslists):
					olist = reslists[ilist]
					ilist += 1
					isValid = True
					if olist["properties"] != None:
						for prop in olist["properties"]:
							if prop["property"].lower() in BLACKLISTED_PROPERTIES:
								isValid = False
					if isValid:
						for price in olist["prices"]:
							if price["type"].lower() == "currency":
								prices.append(int(price["quantity"] / olist["amount"]))
			status = 200
		else:
			status = request.status_code
			break

		expReqs = (elapse / 60) * REQUESTS_PER_MINUTE
		if reqsDone > expReqs:
			waitTime = ((reqsDone / REQUESTS_PER_MINUTE) * 60) - elapse
			time.sleep(waitTime)
		page += 1

	return status, prices

# Below is for testing individual functions
if __name__ == "__main__":
	import os, json

	if not os.path.isdir("testing"):
		os.mkdir("testing")
	if os.path.isdir("testing/fetch"):
		for filename in os.listdir("testing/fetch"):
			os.remove(f"testing/fetch/{filename}")
	else:
		os.mkdir("testing/fetch")

	tcode, tags = fetch_tags()
	if tcode == 200:
		tagCount = 0
		for cat in tags.keys():
			tagCount += len(tags[cat])
		print(f"Successfully got {tagCount} tags across {len(tags)} categories.")
		with open("testing/fetch/tags.json","w") as file:
			file.write(json.dumps(tags))
	else:
		print(f"Failed to get tags; the provided status code is {tcode}.")

	icode, items, iend = fetch_items()
	if len(items) != 0:
		itemCount = 0
		for cat in items.keys():
			itemCount += len(items[cat])
		print(f"Successfully got {itemCount} items across {len(items)} categories.")
		with open("testing/fetch/items.json","w") as file:
			file.write(json.dumps(items))
	else:
		print(f"Failed to get items; the final status code was {icode}.")
	if not iend: print("The end of the items list was not reached.")
