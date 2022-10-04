import requests
import os

# getting the API-Key which is stored in the environment variables 
api_key = os.environ.get('SD_API_Key')


url = "https://api.sportsdata.io/v3/nfl/scores/json/TeamSeasonStats/{2021}"

payload={}
headers = {
    'Ocp-Apim-Subscription-Key': f'{api_key}'
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)

res_json = response.json()

