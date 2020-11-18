import json

with open('meta_Kindle_Store.json') as json_file:
    data = json.load(json_file)
    print (data)