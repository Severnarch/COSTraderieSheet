// Constants
const sheetsUrl = "sheets/";

function camelToTitle(val) {
	val = val.replace(/([A-Z])/g, " $1");
	val = val.charAt(0).toUpperCase() + val.slice(1)
	return val;
}
function formatString(val) {
	val = val.replace(/\w[a-z]*/g, function(x){return x.charAt(0).toUpperCase()+x.substr(1).toLowerCase();});
	val = val.charAt(0).toUpperCase() + val.slice(1)
	val = val.replace("Avg", "Average")
	return val;
}

async function main() {
	// Setup data
	var itemsSheet = [];

	// Fetch data
	try {
		const response = await fetch(sheetsUrl+"items.csv");
		if (!response.ok) {
			console.log(`Fetching CSV file returned ${response.status}`);
		}

		const result = await response.text();
		if (result) {
			rows = result.split("\r\n");
			headers = rows[0].split(",");

			for (i = 1; i < rows.length; i++) {
				if (rows[i].length > 0) {
					const robj = rows[i].split(",");
					var obj = {};
					for (j = 0; j < robj.length; j++) {
						obj[headers[j]] = robj[j];
					}
					itemsSheet.push(obj);
				}
			}
		}
	} catch (error) {
		console.log(error);
	}

	const tableHolder = document.getElementById("table-holder");
	if (itemsSheet.length > 0) {
		var tableElement = document.createElement("table");

		var headerRow = document.createElement("tr");
		var excludedHeaders = ["id", "rawPricesCount", "filterPricesCount"]
		for (i in headers) {
			if (excludedHeaders.includes(headers[i])) {
				continue;
			}
			var headerCell = document.createElement("th");
			headerCell.innerText = camelToTitle(headers[i]);
			headerRow.appendChild(headerCell);
		}
		tableElement.appendChild(headerRow);

		for (i in itemsSheet) {
			var itemRow = document.createElement("tr");

			for (j in headers) {
				if (excludedHeaders.includes(headers[j])) {
					continue;
				}
				var itemCell = document.createElement("td");
				itemCell.innerText = formatString(itemsSheet[i][headers[j]])
				itemRow.appendChild(itemCell);
			}

			tableElement.appendChild(itemRow);
		}

		tableHolder.appendChild(tableElement);
	}
}

window.addEventListener('load', main);