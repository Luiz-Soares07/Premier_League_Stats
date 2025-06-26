import pandas as pd
import json
import os
from typing import List, Dict

DATA_RAW_DIR = 'data/raw'
DATA_PROCESSED_DIR = 'data/processed'


def load_json(path: str) -> List[Dict]:

    try:
        with open(path, "r", encoding = 'utf-8') as f:
            dados = json.load(f)
            return dados
    except Exception as e:
        print(f"Error to load path {path}: {e}")
        return []
    
def extract_datas(fixtures: List[Dict]) -> pd.DataFrame:
    list_of_dicts = []

    for match in fixtures:
        try:

            fixture = match["fixture"]
            teams = match["teams"]
            score = match["score"]
            goals = match["goals"]
            venue = fixture["venue"]
            status = fixture["status"]  
            league = match["league"]
            match_data = {
                "match_id": fixture["id"],
                "date": fixture["date"],
                "stadium": venue["name"],
                "city": venue["city"],
                "referee": fixture["referee"],
                "season": league["season"],
                "round": league["round"],
                "home_team": teams["home"]["name"],
                "away_team": teams["away"]["name"],
                "goals_home": goals["home"],
                "goals_away": goals["away"],
                "score_home_in_half_time": score["halftime"]["home"],
                "score_away_in_half_time": score["halftime"]["away"],
                "score_home_in_full_time": score["fulltime"]["home"],
                "score_away_in_full_time": score["fulltime"]["away"],
                "score_home_in_extra_time": score["extratime"]["home"],
                "score_Away_in_extra_time": score["extratime"]["away"],
                "score_home_in_penalties": score["penalty"]["home"],
                "score_Away_in_penalties": score["penalty"]["away"],
                "elapsed_time": status["elapsed"],
                "extra_time": status["extra"],
                "winner_name":(
                    teams["home"]["name"] if teams["home"]["winner"] else
                    teams["away"]["name"] if teams["away"]["winner"] else
                    "Draw"
                ),
                "status": status["long"],
            }

            list_of_dicts.append(match_data)
        except Exception as e:
            print(f"Error to process {match['fixture']['id']}: {e}")
            continue
    return pd.DataFrame(list_of_dicts)

def save_csv(df: pd.DataFrame, name_path: str):

    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
    path = os.path.join(DATA_PROCESSED_DIR, name_path)
    df.to_csv(path, index=False, encoding='utf-8')
    print(f"File save in: {path}")

def main(season: int):
    file_json = os.path.join(DATA_RAW_DIR, f'fixtures_{season}.json')
    fixtures = load_json(file_json)
    if not fixtures:
        print(f"No data found in {file_json}")
        return
    
    df = extract_datas(fixtures)
    save_csv(df, f"fixtures_season_{season}.csv")

if __name__ == "__main__":
    for year in [2021,2022,2023]:
        print(f"Processing data for season {year}")
        main(year)
    print("Data processing completed.")