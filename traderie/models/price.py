# The code for this API is licensed under the MIT License
# The original source code for this API can be found here:
# https://github.com/Severnarch/COSTraderieSheet

from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True, frozen=True)
class Price():
	"""
	Represents a Traderie price, which can be a currency or an item.

	Attributes:
		id (int): Unique numerical identifier used in API calls
		quantity (int): Amount of self specified
		name (str): User-friendly name of the price, e.g. currency name or item name
		slug (str): URL-friendly name of the price
		isCurrency (bool): Whether the price is a currency (True) or item (False)
		properties (list): Only if item; properties of the item (such as traits)
	"""
	id: int
	quantity: int
	name: str
	slug: str
	isCurrency: bool
	properties: Optional[list]