from dotenv import load_dotenv
import requests
import json
import os
import time

load_dotenv()

API_KEY = os.getenv('API_FOOTBALL_KEY')

#This script collects football match fixtures from API-Football
url = 'https://v3.football.api-sports.io/fixtures' 

#API KEY for API-Football (My persnonal key, please use your own)
headers = {
    'x-apisports-key': API_KEY,  # Replace with your actual API key
    }

# Create the repository if it doesn't exist
os.makedirs('data/raw', exist_ok=True)


#Selection the seasons to collect data
for season in [2021,2022,2023]:
    params = {
        'season': season,
        'league': 39,  # Premier League
        'timezone': 'America/Sao_Paulo',
    }

    #make the request to the API
    response = requests.get(url, headers=headers, params=params)


    #Check if the request was successful
    if response.status_code == 200:
        # Trasnform JSON into a Python dictionary
        data = response.json()

        # Extract the fixtures from the response and save them to a file
        fixtures = data.get('response', [])

        if fixtures:
            file_path = f'data/raw/fixtures_{season}.json'
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(fixtures, f,ensure_ascii=False, indent=4)

            print(f"Temporada {season} salva com sucesso em {file_path} com {len(fixtures)} partidas.")
            
            # Optional: Sleep to avoid hitting API rate limits
            time.sleep(2)

        else:
            print(f"Nenhuma partida encontrada para a temporada {season}.")

    else:
        print(f"Erro na requisção para a temporada {season}: {response.status_code} - {response.text}")


