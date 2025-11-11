// Constants
const sheetsUrl = "sheets/";

async function main() {
	// Setup data
	var itemsSheet = [];

	// Fetch data
	try {
		const response = await fetch(sheetsUrl+"items.csv");
		if (!response.ok) {
			throw new Error(`Response status: ${response.status}`)
		}

		const result = await response.text();
		if (result) {
			result.then(raw=>{
				rows = raw.split("\r\n")
				headers = rows[0].split(",")
				for (i = 1; i < rows.length; i++) {
					if (rows[i].length > 0) {
						const robj = rows[i].split(",")
						var obj = {}
						for (j = 0; j < robj.length; j++) {
							obj[headers[j]] = robj[j]
						}
						itemsSheet.append(obj)
					}
				}
			});
		}
	} catch (error) {
		throw new Error("Error fetching data:", error)
	}

	console.log()
}

window.addEventListener('load', main);