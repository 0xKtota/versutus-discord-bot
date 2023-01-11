import requests
import json

shitcointokenlist = "https://raw.githubusercontent.com/traderjoe-xyz/joe-tokenlists/main/mc.tokenlist.json"
resp = requests.get(shitcointokenlist)
jsonDict = json.loads(resp.text)
#print (jsonDict)
tokens = jsonDict['tokens']['name'].keys()
print(tokens)
# for key in jsonDict:
#     for key,value in jsonDict.items():
#         print("key: {} | value: {}".format(key, value))
#         print()
#         #print(f'key: ')