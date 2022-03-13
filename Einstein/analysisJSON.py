import json

source = open( './result.json', 'r')
json_source = json.load( source )

print( json_source['probabilities'][0]['label'].split(',')[0] )

print( json.dumps(json_source, indent=4) )