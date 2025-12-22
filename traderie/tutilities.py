# The code for this API is licensed under the MIT License
# The original source code for this API can be found here:
# https://github.com/Severnarch/COSTraderieSheet

from urllib.parse import quote

def slugify(toslug:str):
	return ''.join( filter( str.isalnum, toslug.lower() ) )

def addParamsToUrl(url:str, params:dict):
	paramStr = "?"
	for key in params.keys():
		paramStr += quote( key ) + "=" + quote( params[key] ) + "&"
	paramStr = paramStr[:-1]
	return url + paramStr