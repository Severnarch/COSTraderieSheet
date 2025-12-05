# The code for this API is licensed under the MIT License
# The original source code for this API can be found here:
# https://github.com/Severnarch/COSTraderieSheet

from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True, frozen=True)
class Product():
	"""
	Represents a Traderie product, typically an item

	Attributes:
		id (int): Unique numerical identifier of the product used in API calls
		name (str): User-friendly name of the product
		slug (str): URL-friendly name of the product
		description (str): Optional description of the product
		category (str): Singular category the product fits into
	"""

	id: int
	name: str
	slug: str
	description: Optional[str]
	category: str