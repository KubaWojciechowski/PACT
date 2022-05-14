import csv, json

csvFilePath = 'examples/example.csv'
jsonOutput = 'examples/example.json'

data = []
with open(csvFilePath) as csvFile:
	csvReader = csv.DictReader(csvFile)
	for rows in csvReader:
		data.append(rows)

with open(jsonOutput, 'w') as jsonFile:
	jsonFile.write(json.dumps(data, indent=4))

