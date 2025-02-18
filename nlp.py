import spacy
import data
import json

nlp = spacy.load("./nba_ruler")

with open("data/stats_abbr.json", "r", encoding="utf-8") as file:
    stats_abbr = json.load(file)

def classify(doc):
    
    goal = None
    name = None
    stat = None
    stat_name = None
    entities = {ent.label_: ent.text for ent in doc.ents}
    if "PLAYER" in entities and "STAT" in entities:
        name = entities["PLAYER"].lower()
        stat_name = entities["STAT"].lower()
        stat = stats_abbr[stat_name]
        goal = "P_STATS"
    
    return goal, name, stat, stat_name
    
    
def proc(txt: str):
    doc = nlp(txt)
    entities = {ent.label_: ent.text for ent in doc.ents}
    if "PLAYER" not in entities and "TEAM" not in entities:
        return "I'm sorry, I was unable to identify the player or team in your question. Please ask a statistical question containing a player or team name in the 2024 NBA season."
    if "STAT" not in entities and "PLAYER" in entities or "TEAM" in entities:
        return "I'm sorry, I was unable to identify the statistic in your question. Please ask a question containing a statistic for {}.".format(entities["PLAYER"] if "PLAYER" in entities else entities["TEAM"])
    
    goal, name, stat, stat_name = classify(doc)

    if goal != None:
        
        if goal == "P_STATS":
            season = "2024-25"
            player_name = name
            response = None
            player_id = data.get_player_id(player_name)
            if player_id:
                if stat:
                    season_stat = data.p_stats_season(player_id, season, stat)
                    pergame_stat = data.p_stats_per_game(player_id, season, stat)
                    response = "In the 2024 season {} averaged {:.2f} {} per game. His current total {} for the season is {}.".format(player_name.title(), float(pergame_stat), stat_name, stat_name, season_stat)
            return response
    else:
        return "I'm sorry, I don't understand your question."

# response = proc("How many rebounds did Trae Young average in 2024?")
# print(response)
# response = proc("How many assists did Stephen Curry average in 2024?")
# print(response)
# response = proc("Who is Stephen Curry?")
# print(response)