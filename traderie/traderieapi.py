# The code for this API is licensed under the MIT License
# The original source code for this API can be found here:
# https://github.com/Severnarch/COSTraderieSheet

from .models.price import Price
from .models.product import Product
from .models.seller import Seller

from .tutilities import slugify, addParamsToUrl
import cloudscraper

class TraderieAPI():
	"""
	Main class for interacting with the Traderie API

	Methods:
		__init__(str): Create a new TraderieAPI instance assigned with a game slug
		searchItems(str): Search items with a query
	"""

	_baseUrl = "https://traderie.com/api/{}/{}"

	def __init__(self, gameSlug:str):
		self.scraper = cloudscraper.create_scraper()
		self.gameSlug = slugify( gameSlug )

	def _getUrlForRequest(self, reqType:str):
		return self._baseUrl.format( self.gameSlug, reqType.lower() )

	def searchItems(self, query:str):
		querySlug = slugify( query )
		rawUrl = self._getUrlForRequest( "items" )
		reqUrl = addParamsToUrl( rawUrl, { "search": querySlug } )

		request = self.scraper.get( reqUrl )
		content = request.json()

		retlist = []
		for item in content["items"]:
			product = Product(
				item["id"], 
				item["name"], 
				item["slug"], 
				item["description"] or "", 
				item["type"]
			)
			retlist.append(product)

		return retlist