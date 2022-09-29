import requests
import os

# getting the API-Key which is stored in the environment variables 
api_key = os.environ.get('SD_API_Key')
print(api_key)


# url = "https://api.sportsdata.io/v3/nfl/scores/json/Stadiums"

# payload={}
# headers = {
#   'Ocp-Apim-Subscription-Key': '{}'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)