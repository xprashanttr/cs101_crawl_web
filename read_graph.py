import json

with open('graph.datax', 'r') as handle:
	parsed = json.load(handle)
	print(json.dumps(parsed, indent=4, sort_keys=True))

