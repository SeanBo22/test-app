import pandas as pd
from nba_api.stats.endpoints import playercareerstats
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

''''
    PLAYER_ID SEASON_ID LEAGUE_ID     TEAM_ID TEAM_ABBREVIATION  PLAYER_AGE  GP  GS     MIN  FGM   FGA  FG_PCT  FG3M  FG3A  FG3_PCT  FTM  FTA  FT_PCT  OREB  DREB  REB  AST  STL  BLK  TOV   PF   PTS
0      203076   2012-13        00  1610612740               NOH        20.0  64  60  1846.0  349   676   0.516     0     6    0.000  169  225   0.751   165   357  522   63   75  112   89  158   867
1      203076   2013-14        00  1610612740               NOP        21.0  67  66  2358.0  522  1005   0.519     2     9    0.222  348  440   0.791   207   466  673  105   89  189  109  200  1394
2      203076   2014-15        00  1610612740               NOP        22.0  68  68  2455.0  642  1199   0.535     1    12    0.083  371  461   0.805   173   523  696  149  100  200   95  141  1656
3      203076   2015-16        00  1610612740               NOP        23.0  61  61  2164.0  560  1136   0.493    35   108    0.324  326  430   0.758   130   497  627  116   78  125  121  148  1481
4      203076   2016-17        00  1610612740               NOP        24.0  75  75  2708.0  770  1526   0.505    40   134    0.299  519  647   0.802   172   712  884  157   94  167  181  168  2099
5      203076   2017-18        00  1610612740               NOP        25.0  75  75  2727.0  780  1462   0.534    55   162    0.340  495  598   0.828   187   644  831  174  115  193  162  159  2110
6      203076   2018-19        00  1610612740               NOP        26.0  56  56  1850.0  530  1026   0.517    48   145    0.331  344  433   0.794   174   498  672  218   88  135  112  132  1452
7      203076   2019-20        00  1610612747               LAL        27.0  62  62  2131.0  551  1096   0.503    72   218    0.330  444  525   0.846   142   435  577  200   91  143  154  156  1618
8      203076   2020-21        00  1610612747               LAL        28.0  36  36  1162.0  301   613   0.491    26   100    0.260  158  214   0.738    62   224  286  110   45   59   74   60   786
9      203076   2021-22        00  1610612747               LAL        29.0  40  40  1404.0  370   695   0.532    13    70    0.186  174  244   0.713   106   288  394  122   49   90   82   97   927
10     203076   2022-23        00  1610612747               LAL        30.0  56  54  1905.0  542   962   0.563    19    74    0.257  348  444   0.784   195   507  702  148   59  114  122  146  1451
11     203076   2023-24        00  1610612747               LAL        31.0  76  76  2700.0  713  1283   0.556    29   107    0.271  421  516   0.816   239   722  961  266   91  178  159  177  1876
12     203076   2024-25        00  1610612747               LAL        31.0  42  42  1439.0  400   758   0.528    28    94    0.298  253  321   0.788   119   380  499  141   54   90   93   82  1081
'''

with open("data/player_ids.json", "r", encoding="utf-8") as file:
        player_ids = json.load(file)

# Helper function to get player ID using fuzzy matching
def get_player_id(player_name: str):
    # Get a list of player names from the player_ids JSON
    player_names = list(player_ids.keys())
    
    # Find the best match using fuzzy matching
    best_match, score = process.extractOne(player_name, player_names, scorer=fuzz.token_sort_ratio)
    
    # If the match score is above a certain threshold, return the player ID
    if score >= 80:  # You can adjust this threshold based on your needs
        return player_ids[best_match]
    else:
        return None  # If no good match is found
    
def p_stats_per_game(player_id, season, stat):
    # Fetch Anthony Davis' career stats 203076
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)

    # Get the JSON response and parse it
    career_stats = career_stats.get_json()
    career_stats = json.loads(career_stats)

    # Extract column headers and data
    headers = career_stats["resultSets"][0]["headers"]
    row_set = career_stats["resultSets"][0]["rowSet"]

    # Create a DataFrame
    df = pd.DataFrame(row_set, columns=headers)

    # Make a copy of the DataFrame to avoid the warning
    season_stats = df[df["SEASON_ID"] == season].copy()

    # Calculate PPG for the 2024-25 season
    season_stats[stat] = season_stats[stat] / season_stats["GP"]

    # Display the PPG for 2024-25
    return season_stats[stat].values[0]

def p_stats_season(player_id, season, stat):
    # Fetch Anthony Davis' career stats 203076
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)

    # Get the JSON response and parse it
    career_stats = career_stats.get_json()
    career_stats = json.loads(career_stats)

    # Extract column headers and data
    headers = career_stats["resultSets"][0]["headers"]
    row_set = career_stats["resultSets"][0]["rowSet"]

    # Create a DataFrame
    df = pd.DataFrame(row_set, columns=headers)

    # Make a copy of the DataFrame to avoid the warning
    season_stats = df[df["SEASON_ID"] == season].copy()

    # Display the PPG for 2024-25
    return season_stats[stat].values[0]


# stats_per_game("203076", "2024-25", "REB")
# stats_season("203076", "2024-25", "REB")





