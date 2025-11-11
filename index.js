// Constants
const sheetsUrl = "sheets/";

async function main() {
	// Setup data
	var itemsSheet = {};

	try {
		const itemsResponse = await fetch(sheetsUrl+"items.csv");
		if (!response.ok) {
			throw new Error(`Response status: ${response.status}`)
		}

		const result = await response.text();
		console.log(result)
	} catch (error) {
		throw new Error("Error fetching a file:", error)
	}
}

window.addEventListener('load', main);