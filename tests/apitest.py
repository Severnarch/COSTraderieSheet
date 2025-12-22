# This code is licensed under the MIT License
# The original source code can be found here:
# https://github.com/Severnarch/COSTraderieSheet

import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from traderie.traderieapi import TraderieAPI

if __name__ == "__main__":
	instance = TraderieAPI( "creaturesofsonaria" )

	adharcQuery = instance.searchItems( "adharc" )
	print(adharcQuery)