# The code for this API is licensed under the MIT License
# The original source code for this API can be found here:
# https://github.com/Severnarch/COSTraderieSheet

from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True, frozen=True)
class Seller():
	"""
	Represents a Traderie seller

	Attributes:
		id (int): Unique numerical identifier of the seller used in API calls
		name (str): Username of the seller
		description (str): Optional description of the seller (internally "bio")
		rating (float): Optional rating out of 5 of the seller
	"""

	id: int
	name: str
	description: Optional[str]
	rating: Optional[float]