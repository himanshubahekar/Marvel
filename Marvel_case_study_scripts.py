import requests
import os
import hashlib
import json
import pandas as pd
from time import time
import string
from asyncio.windows_events import NULL

#Activity 2
api_url = "http://gateway.marvel.com/v1/public/"
api_url_2 = "characters"
address = api_url + api_url_2
public_key = 'de89122dc1714c3f5adfea57a25e1474'
private_key = '01e29808b84258314ea1c092c14d69131df221cc'
limit = 100 

ts = str(int(time()))
hash_param = ts+private_key+public_key
hash_result = hashlib.md5(hash_param.encode())

params = {"apikey": public_key, 
            "ts": int(time()), 
            "hash": hash_result.hexdigest(),
            "limit": limit}

start_char = list(string.ascii_lowercase + string.digits)
start_char.remove('0')

df = pd.DataFrame()

for letter in start_char :
    params["nameStartsWith"] = letter
    response = requests.get(address, params)
    temp_df = pd.json_normalize(response.json(), record_path=['data', 'results'])
    df = pd.concat([df, temp_df], ignore_index=True)
    del params["nameStartsWith"]

#Activity 3
def get_df(nameStartWith, apikey, hash):
    
	"""
	returns a dataframe where character name starts with a specific string
	"""

	# if(apikey==NULL or md5hash==NULL):
	# 	raise Exception ("Hash and/or API key is not provided")
	api_url = "http://gateway.marvel.com/v1/public/character"

	try:
		params = {"apikey": apikey, "ts": int(time()), 
				"hash": hash, "nameStartsWith": nameStartWith,
				"limit" : 100}

		response = requests.get(api_url, params)
		df = pd.json_normalize(response.json(), record_path=['data','results'])
		return df
	except:
		print("Hash and/or API key is not provided")  

#Activity 4
def ch_filter(df1,col,filter_condition):
    return df1.query(col+filter_condition)

#Activity 5
import argparse
api_key = public_key
hash = hash_result
parser = argparse.ArgumentParser(description='Activity')
parser.add_argument("-apikey", "--api_key", help="adds api_key", default= NULL)
parser.add_argument("-hash", "--hash", help="adds hash", default= NULL)
args, unknown = parser.parse_known_args()   #add CLI arguements while executing in CLI

print("API KEY",args.api_key)
print("HASH",args.hash)
api_key = args.api_key
hash = args.hash 