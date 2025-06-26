import pandas as pd
from typing import List, Dict

def calculate_team_stats(df: pd.DataFrame) -> pd.DataFrame:


    stats: List[Dict] = []
    seasons = df['season'].unique()

    for season in seasons:
        season_df = df[df["season"] == season]

        teams = pd.unique(season_df[["home_team", "away_team"]].values.ravel())

        for team in teams:
            team_stats = {
                "season": season,
                "team": team,
                "games_played": 0,
                "home_games_played": 0,
                "away_games_played": 0,
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "wins_home": 0,
                "wins_away": 0,
                "losses_home": 0,
                "losses_away": 0,
                "draws_home": 0,
                "draws_away": 0,
                "goals_score_total": 0,
                "conceded_total": 0,
                "goals_home": 0,
                "goals_away": 0,
                "conceded_home": 0,
                "conceded_away": 0,
                "goals_first_time_total": 0,
                "goals_second_time_total": 0,
                "goals_first_time_home": 0,
                "goals_first_time_away": 0,
                "goals_second_time_home": 0,
                "goals_second_time_away": 0,
                "goals_difference": 0,
                "points": 0,
                "win_rate_home": 0.0,
                "win_rate_away": 0.0,
                "win_rate": 0.0,
                "loss_rate_home": 0.0,
                "loss_rate_away": 0.0,
                "loss_rate": 0.0,
                "draw_rate_home": 0.0,
                "draw_rate_away": 0.0,
                "draw_rate": 0.0,
                "clean_sheets": 0,
                "goals_conceded_per_game": 0.0,
                "goals_conceded_per_game_home": 0.0,
                "goals_conceded_per_game_away": 0.0,
                "goals_scored_per_game": 0.0,
                "goals_scored_per_game_home": 0.0,
                "goals_scored_per_game_away": 0.0,
                "failed_to_score": 0,  
            }
            home = season_df[season_df["home_team"] == team]
            team_stats["home_games_played"] = len(home)
            team_stats["draws_home"] = len(home[home["winner_name"] == "Draw"])
            team_stats["wins_home"] = len(home[home["winner_name"] == team])
            team_stats["losses_home"] = len(home[home["winner_name"] != team]) - team_stats["draws_home"]
            team_stats["goals_home"] = home["goals_home"].fillna(0).sum()
            team_stats["conceded_home"] = home["goals_away"].fillna(0).sum()
            team_stats["goals_first_time_home"] = home["score_home_in_half_time"].fillna(0).sum()
            team_stats["goals_second_time_home"] = home["score_home_in_full_time"].fillna(0).sum() - team_stats["goals_first_time_home"]
            team_stats["win_rate_home"] = team_stats["wins_home"] / team_stats["home_games_played"] if team_stats["home_games_played"] > 0 else 0.0
            team_stats["loss_rate_home"] = team_stats["losses_home"] / team_stats["home_games_played"] if team_stats["home_games_played"] > 0 else 0.0  
            team_stats["draw_rate_home"] = team_stats["draws_home"] / team_stats["home_games_played"] if team_stats["home_games_played"] > 0 else 0.0
            team_stats["goals_scored_per_game_home"] = (team_stats["goals_home"] / team_stats["home_games_played"]
                                                        if team_stats["home_games_played"] > 0 else 0.0)
            team_stats["goals_conceded_per_game_home"] = (team_stats["conceded_home"] / team_stats["home_games_played"]
                                                        if team_stats["home_games_played"] > 0 else 0.0)
                                                        

            away = season_df[season_df["away_team"] == team]
            team_stats["away_games_played"] = len(away)
            team_stats["draws_away"] = len(away[away["winner_name"] == "Draw"])
            team_stats["wins_away"] = len(away[away["winner_name"] == team])
            team_stats["losses_away"] = len(away[away["winner_name"] != team]) - team_stats["draws_away"]
            team_stats["goals_away"] = away["goals_away"].fillna(0).sum()
            team_stats["conceded_away"] = away["goals_home"].fillna(0).sum()
            team_stats["goals_first_time_away"] = away["score_away_in_half_time"].fillna(0).sum()
            team_stats["goals_second_time_away"] = away["score_away_in_full_time"].fillna(0).sum() - team_stats["goals_first_time_away"]
            team_stats["win_rate_away"] = team_stats["wins_away"] / team_stats["away_games_played"] if team_stats["away_games_played"] > 0 else 0.0
            team_stats["loss_rate_away"] = team_stats["losses_away"] / team_stats["away_games_played"] if team_stats["away_games_played"] > 0 else 0.0
            team_stats["draw_rate_away"] = team_stats["draws_away"] / team_stats["away_games_played"] if team_stats["away_games_played"] > 0 else 0.0
            team_stats["goals_scored_per_game_away"] = (team_stats["goals_away"] / team_stats["away_games_played"]
                                                        if team_stats["away_games_played"] > 0 else 0.0)
            team_stats["goals_conceded_per_game_away"] = (team_stats["conceded_away"] / team_stats["away_games_played"]
                                                        if team_stats["away_games_played"] > 0 else 0.0)

            team_stats["games_played"] = team_stats["home_games_played"] + team_stats["away_games_played"]
            team_stats["wins"] = team_stats["wins_home"] + team_stats["wins_away"]
            team_stats["losses"] = team_stats["losses_home"] + team_stats["losses_away"]
            team_stats["draws"] = team_stats["draws_home"] + team_stats["draws_away"]
            team_stats["goals_score_total"] = team_stats["goals_home"] + team_stats["goals_away"]
            team_stats["conceded_total"] = team_stats["conceded_home"] + team_stats["conceded_away"]
            team_stats["goals_first_time_total"] = team_stats["goals_first_time_home"] + team_stats["goals_first_time_away"]
            team_stats["goals_second_time_total"] = team_stats["goals_second_time_home"] + team_stats["goals_second_time_away"]
            team_stats["goals_difference"] = team_stats["goals_score_total"] - team_stats["conceded_total"]
            team_stats["points"] = team_stats["wins"] * 3 + team_stats["draws"] * 1 
            team_stats["win_rate"] = team_stats["wins"] / team_stats["games_played"] if team_stats["games_played"] > 0 else 0.0
            team_stats["loss_rate"] = team_stats["losses"] / team_stats["games_played"] if team_stats["games_played"] > 0 else 0.0
            team_stats["draw_rate"] = team_stats["draws"] / team_stats["games_played"] if team_stats["games_played"] > 0 else 0.0
            team_stats["clean_sheets"] = (len(season_df[((season_df["home_team"] == team)) & (season_df["goals_away"] == 0)])+ 
                                        len(season_df[((season_df["away_team"] == team)) & (season_df["goals_home"] == 0)]))
            team_stats["goals_conceded_per_game"] = (team_stats["conceded_total"] / team_stats["games_played"] 
                                                    if team_stats["games_played"] > 0 else 0.0)
            team_stats["failed_to_score"] = (len(season_df[((season_df["home_team"] == team) & (season_df["goals_home"] == 0))]) +
                                                 (len(season_df[((season_df["away_team"] == team)) & (season_df["goals_away"] == 0)])))
            
            stats.append(team_stats)

    team_stats_df = pd.DataFrame(stats)
    return team_stats_df.sort_values(by=["season", "team"]).reset_index(drop=True)

        
        
        
        
        

    


