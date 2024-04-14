import os
import json
from functions import *

dataRootDirectory = "put the path to the data folder of the opendata file structure here"

eventsDirectory =  dataRootDirectory + "events"
lineupsDirectory = dataRootDirectory + "lineups"
matchesDirectory = dataRootDirectory + "matches"
threeSixtyDirectory = dataRootDirectory + "three-sixty"
competitionsFile = dataRootDirectory + "competitions.json"

competitions = []
def loadCompetitionFileData(competitionsFile):
    currfile = open(competitionsFile, encoding="utf8")
    competitonsList = json.load(currfile)
    currfile.close()
    usedCompetitionIds = []

    for competition in competitonsList:
        if "competition_name" in competition and ('La Liga' == competition["competition_name"] or "Premier League" == competition["competition_name"]):
            if "season_name" in competition and (("2020/2021" in competition["season_name"]) or ("2003/2004" in competition["season_name"]) or ("2019/2020" in competition["season_name"]) or ("2018/2019" in competition["season_name"])):
                currCompetition = {"competition_id": competition["competition_id"],
                                "season_id": competition["season_id"],
                                "competition_name": competition["competition_name"],
                                "competition_gender": competition["competition_gender"],
                                "competition_youth": competition["competition_youth"],
                                "competition_international": competition["competition_international"],}
                competitions.append(currCompetition)
                usedCompetitionIds.append(competition["competition_id"])
    return usedCompetitionIds


matches = []
countries = []
teams = []
managers = []
referees = []
seasons = []
stadiums = []
def loadMatchFileData(matchesDirectory, usedCompetitionIds):
    usedMatchIds = []
    for root, dirs, files in os.walk(matchesDirectory):
        for filename in files:
            fullPath = os.path.join(root, filename)
            splitPath = fullPath.split("\\")
            seasonId = splitPath[-1].split(".")[0]
            competitionId = splitPath[-2]
            print("Now Reading:" + str(fullPath))
            if (competitionId == '11' and (seasonId == '4' or seasonId == '42' or seasonId == '90')) or (competitionId == '2' and seasonId == '44'):
                # manually map the values into new dictionaries/json objects and insert those into the database
                currfile = open(fullPath, encoding="utf8")
                matchList = json.load(currfile)
                currfile.close()
                for match in matchList:
                    currMatch = {"match_id": match["match_id"],
                            "competition_id": competitionId,
                            "season_id": match["season"]["season_id"],
                            "match_date": match["match_date"],
                            "kick_off": match["kick_off"],
                            "home_team_id": match["home_team"]["home_team_id"],
                            "away_team_id": match["away_team"]["away_team_id"],
                            "home_score": match["home_score"],
                            "away_score": match["away_score"],
                            "match_week": match["match_week"],
                            "competition_stage": match["competition_stage"]["id"]}
                    usedMatchIds.append(str(match["match_id"]))
                    if "stadium" in match:
                        currMatch["stadium_id"] = match["stadium"]["id"]

                        stadium_used = {"stadium_id": match["stadium"]["id"],
                                    "stadium_name": match["stadium"]["name"],
                                    "country_id": match["stadium"]["country"]["id"],}

                    home_country = {"country_id": match["home_team"]["country"]["id"],
                                "country_name": match["home_team"]["country"]["name"]}
                
                    away_country = {"country_id": match["away_team"]["country"]["id"],
                                "country_name": match["away_team"]["country"]["name"]}
                
                    curr_season = {"season_id": match["season"]["season_id"],
                            "season_name": match["season"]["season_name"]}
                
                    home_team_manager_ids = []
                    away_team_manager_ids = []

                    if "managers" in match["home_team"]:
                        for manager in match["home_team"]["managers"]:
                            home_team_manager_ids.append(manager["id"])
                            new_manager = {"manager_id": manager["id"],
                                    "manager_name": manager["name"],
                                    "manager_nickname": manager["nickname"],
                                    "dob": manager["dob"],
                                    "country_id": manager["country"]["id"],
                                    }
                            manager_home_country = {"country_id": manager["country"]["id"],
                                "country_name": manager["country"]["name"]}
                            managers.append(new_manager)
                            countries.append(manager_home_country)
                    if "managers" in match["away_team"]:
                        for manager in match["away_team"]["managers"]:
                            away_team_manager_ids.append(manager["id"])
                            new_manager = {"manager_id": manager["id"],
                                    "manager_name": manager["name"],
                                    "manager_nickname": manager["nickname"],
                                    "dob": manager["dob"],
                                    "country_id": manager["country"]["id"],
                                    }
                            manager_home_country = {"country_id": manager["country"]["id"],
                                "country_name": manager["country"]["name"]}
                            managers.append(new_manager)
                            countries.append(manager_home_country)
                    home_team = {"team_id": match["home_team"]["home_team_id"],
                            "team_name": match["home_team"]["home_team_name"],
                            "gender": match["home_team"]["home_team_gender"],
                            "team_group": match["home_team"]["home_team_group"],
                            "country_id": match["home_team"]["country"]["id"],
                            "manager_ids": home_team_manager_ids
                            }

                    away_team = {"team_id": match["away_team"]["away_team_id"],
                            "team_name": match["away_team"]["away_team_name"],
                            "gender": match["away_team"]["away_team_gender"],
                            "team_group": match["away_team"]["away_team_group"],
                            "country_id": match["away_team"]["country"]["id"],
                            "manager_ids": away_team_manager_ids
                            }

                    if "referee" in match:
                        currMatch["referee_id"] = match["referee"]["id"]
                        curr_ref = {"referee_id": match["referee"]["id"],
                            "referee_name": match["referee"]["name"],
                            "referee_country": match["referee"]["country"]["id"]}
                        referees.append(curr_ref)

                    matches.append(currMatch)
                    countries.append(home_country)
                    countries.append(away_country)
                    seasons.append(curr_season)
                    teams.append(home_team)
                    teams.append(away_team)
                    stadiums.append(stadium_used)
    return usedMatchIds

def loadIntoTempFile(data_type, files_loaded, data):
    range_val = files_loaded//1000
    if range_val < 1:
        range_val = 1
    with open(data_type + str(range_val) + '.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()

def loadEventsFromTempFiles(files_loaded):
    range_val = files_loaded//1000
    if range_val < 1:
        range_val = 1
    for i in range(range_val):
        file = open("events" + str(range_val) + '.json', encoding="utf8")
        event_data = json.load(file)
        populateEvents(event_data)
        file.close()

def loadTacticsFromTempFiles(files_loaded):
    range_val = files_loaded//1000
    if range_val < 1:
        range_val = 1
    for i in range(range_val):
        file = open("tactics" + str(range_val) + '.json', encoding="utf8")
        tactics_data = json.load(file)
        populateTactics(tactics_data)
        file.close()
        
def loadTypedEventsFromTempFiles(files_loaded):
    range_val = files_loaded//1000
    if range_val < 1:
        range_val = 1
    for i in range(range_val):
        file = open("typed_events" + str(range_val) + '.json', encoding="utf8")
        event_data = json.load(file)
        populateTypedEvents(event_data)
        file.close()


def loadEventFileData(eventsDirectory, usedMatchIds):
    tactic_id_count = 0
    events = []
    tactics = []
    typed_events = []
    files_loaded = 0

    for root, dirs, files in os.walk(eventsDirectory):
        for filename in files:
            fullPath = os.path.join(root, filename)
            splitPath = fullPath.split("\\")
            matchId = splitPath[-1].split(".")[0]
            print("Now Reading:" + str(fullPath))
            if matchId in usedMatchIds:
                files_loaded = files_loaded + 1
                if (files_loaded%1000 == 0):
                    loadIntoTempFile("events", files_loaded, events)
                    loadIntoTempFile("tactics", files_loaded, tactics)
                    loadIntoTempFile("typed_events", files_loaded, typed_events)
                    events = []
                    tactics = []

                # manually map the values into new dictionaries/json objects and insert those into the database
                currfile = open(fullPath, encoding="utf8")
                eventList = json.load(currfile)
                currfile.close()

                for event in eventList:
                    currEvent = {"event_id": event["id"],
                                "event_index": event["index"],
                                "match_id": matchId,
                                "period": event["period"],
                                "event_timestamp": event["timestamp"],
                                "event_minute": event["minute"],
                                "event_second": event["second"],
                                "event_type": event["type"]["id"],
                                "possession": event["possession"],
                                "possession_team": event["possession_team"]["id"],
                                "play_pattern": event["play_pattern"]["id"],
                                "team": event["team"]["id"]}
                    typed_events.append(processTypedEvent(event, event["id"]))
                    if "player" in event:
                        currEvent["player"] = event["player"]["id"]

                    if "position" in event:
                        currEvent["event_position_id"] = event["position"]["id"]

                    if "location" in event:
                        currEvent["event_location"] = event["location"]

                    if "duration" in event:
                        currEvent["duration"] = event["duration"]

                    if "tactics" in event:
                        new_tactic = {"tactic_id": tactic_id_count,
                                    "formation": event["tactics"]["formation"],
                                    "lineup": [event["team"]["id"], matchId]}
                        
                        tactics.append(new_tactic)

                        currEvent["tactics"] = tactic_id_count
                        tactic_id_count += 1

                    events.append(currEvent)
    loadIntoTempFile("events", files_loaded+1000, events)
    loadIntoTempFile("tactics", files_loaded+1000, tactics)
    loadIntoTempFile("typed_events", files_loaded+1000, typed_events)
    return files_loaded     
        

def processTypedEvent(event, event_uuid):
    out = {"event_id": event_uuid,
           "event_type": event["type"]["id"]}

    match event["type"]["id"]:
        case 33:
            if "50_50" in event:
                out["id1"] = event["50_50"]["outcome"]["id"]
                if "counterpress" in event["50_50"]:
                        out["bool1"] =  event["50_50"]["counterpress"]

        case 24:
            if "bad_behavior" in event:
                out["id1"] = event["bad_behavior"]["card"]["id"]

        case 42:
            if "ball_receipt" in event:
                out["id1"] = event["ball_receipt"]["outcome"]["id"]
            
        case 2:
            if "ball_recovery" in event:
                if "offensive" in event["ball_recovery"]:
                    out["bool1"] = event["ball_recovery"]["offensive"]
                if "recovery_failure" in event["ball_recovery"]:
                    out["bool2"] = event["ball_recovery"]["recovery_failure"]
        case 6:
            if "block" in event:
                if "deflection" in event["block"]:
                    out["bool1"] = event["block"]["deflection"]
                if "offensive" in event["block"]:
                    out["bool2"] = event["block"]["offensive"]
                if "save_block" in event["block"]:
                    out["bool3"] = event["block"]["save_block"]
                if "counterpress" in event["block"]:
                    out["bool1"] =  event["block"]["counterpress"]

        case 43:
            if "carry" in event:
                out["location"] = event["carry"]["end_location"]
        
        case 9:
            if "clearance" in event:
                if "aerial_won" in event["clearance"]:
                    out["bool1"] = event["clearance"]["aerial_won"]
                if "body_part" in event["clearance"]:
                    out["id1"] = event["clearance"]["body_part"]["id"]
        
        case 14:
            if "dribble" in event:
                if "overrun" in event["dribble"]:
                    out["bool1"] = event["dribble"]["overrun"]
                if "nutmeg" in event["dribble"]:
                    out["bool2"] = event["dribble"]["nutmeg"]
                out["id1"] = event["dribble"]["outcome"]["id"]
                if "no_touch" in event["dribble"]:
                    out["bool3"] = event["dribble"]["no_touch"]
        
        case 39:
            if "dribbled_past" in event:
                out["bool1"] = event["dribbled_past"]["counterpress"]
        
        case 4:
            if "duel" in event:
                if "counterpress" in event["duel"]:
                    out["bool1"] = event["duel"]["counterpress"]
                if "type" in event["duel"]:
                    out["id1"] = event["duel"]["type"]["id"]
                if "outcome" in event["duel"]:
                    out["id2"] = event["duel"]["outcome"]["id"]
        case 22:
            if "foul_committed" in event:
                if "counterpress" in event["foul_committed"]:
                    out["bool1"] = event["foul_committed"]["counterpress"]
                if "offensive" in event["foul_committed"]:
                    out["bool2"] = event["foul_committed"]["offensive"]
                if "type" in event["foul_committed"]:
                    out["id1"] = event["foul_committed"]["type"]["id"]
                if "advantage" in event["foul_committed"]:
                    out["bool3"] = event["foul_committed"]["advantage"]
                if "penalty" in event["foul_committed"]:
                    out["bool4"] = event["foul_committed"]["penalty"]
                if "card" in event["foul_committed"]:
                    out["id2"] = event["foul_committed"]["card"]["id"]
        
        case 21:
            if "foul_won" in event:
                if "defensive" in event["foul_won"]:
                    out["bool1"] = event["foul_won"]["defensive"]
                if "advantage" in event["foul_won"]:
                    out["bool2"] = event["foul_won"]["advantage"]
                if "penalty" in event["foul_won"]:
                    out["bool3"] = event["foul_won"]["penalty"]
        case 23:
            if "goalkeeper" in event:
                if "position" in event["goalkeeper"]:
                    out["id1"] = event["goalkeeper"]["position"]["id"]
                if "technique" in event["goalkeeper"]:
                    out["id2"] = event["goalkeeper"]["technique"]["id"]
                if "body_part" in event["goalkeeper"]:
                    out["id3"] = event["goalkeeper"]["body_part"]["id"]
                if "type" in event["goalkeeper"]:
                    out["id4"] = event["goalkeeper"]["type"]["id"]
                if "outcome" in event["goalkeeper"]:
                    out["id5"] = event["goalkeeper"]["outcome"]["id"]
        
        case 34:
            if "half_end" in event:
                if "early_video_end" in event["half_end"]:
                    out["bool1"] = event["half_end"]["early_video_end"]
                if "match_suspended" in event["half_end"]:
                    out["bool2"] = event["half_end"]["match_suspended"]
        
        case 18:
            if "half_start" in event:
                if "late_video_start" in event["half_start"]:
                    out["bool1"] = event["half_start"]["late_video_start"]
        
        case 40:
            if "injury_stoppage" in event:
                if "in_chain" in event["injury_stoppage"]:
                    out["bool1"] = event["injury_stoppage"]["in_chain"]
        
        case 10:
            if "interception" in event:
                if "outcome" in event["interception"]:
                    out["id1"] = event["interception"]["outcome"]["id"]
        
        case 38:
            if "miscontrol" in event:
                if "aerial_won" in event["miscontrol"]:
                    out["bool1"] = event["miscontrol"]["aerial_won"]
        
        case 30:
            if "pass" in event:
                if "recipient" in event["pass"]:
                    out["id1"] = event["pass"]["recipient"]["id"]
                if "length" in event["pass"]:
                    out["decimal1"] = event["pass"]["length"]
                if "angle" in event["pass"]:
                    out["decimal2"] = event["pass"]["angle"]
                if "height" in event["pass"]:
                    out["id2"] = event["pass"]["height"]["id"]
                if "end_location" in event["pass"]:
                    out["location"] = event["pass"]["end_location"]
                if "assisted_shot" in event["pass"]:
                    out["related_uuid"] = event["pass"]["assisted_shot"]
                if "backheel" in event["pass"]:
                    out["bool1"] = event["pass"]["backheel"]
                if "deflected" in event["pass"]:
                    out["bool2"] = event["pass"]["deflected"]
                if "miscommunication" in event["pass"]:
                    out["bool3"] = event["pass"]["miscommunication"]
                if "cross" in event["pass"]:
                    out["bool4"] = event["pass"]["cross"]
                if "cut_back" in event["pass"]:
                    out["bool5"] = event["pass"]["cut_back"]
                if "switch" in event["pass"]:
                    out["bool6"] = event["pass"]["switch"]
                if "shot_assist" in event["pass"]:
                    out["bool7"] = event["pass"]["shot_assist"]
                if "goal_assist" in event["pass"]:
                    out["bool8"] = event["pass"]["goal_assist"]
                if "body_part" in event["pass"]:
                    out["id3"] = event["pass"]["body_part"]["id"]
                if "type" in event["pass"]:
                    out["id4"] = event["pass"]["type"]["id"]
                if "outcome" in event["pass"]:
                    out["id5"] = event["pass"]["outcome"]["id"]
                if "technique" in event["pass"]:
                    out["id6"] = event["pass"]["technique"]["id"]
        
        case 27:
            if "player_off" in event:
                if "permanent" in event["player_off"]:
                    out["bool1"] = event["player_off"]["permanent"]
        
        case 17:
            if "pressure" in event:
                if "counterpress" in event["pressure"]:
                    out["bool1"] = event["pressure"]["counterpress"]
        
        case 16:
            if "shot" in event:
                if "key_pass_id" in event["shot"]:
                    out["uuid"] = event["shot"]["key_pass_id"]
                if "end_location" in event["shot"]:
                    out["location"] = event["shot"]["end_location"]
                if "aerial_won" in event["shot"]:
                    out["bool1"] = event["shot"]["aerial_won"]
                if "follows_dribble" in event["shot"]:
                    out["bool2"] = event["shot"]["follows_dribble"]
                if "first_time" in event["shot"]:
                    out["bool3"] = event["shot"]["first_time"]
                if "open_goal" in event["shot"]:
                    out["bool4"] = event["shot"]["open_goal"]
                if "statsbomb_xg" in event["shot"]:
                    out["xg_score"] = event["shot"]["statsbomb_xg"]
                if "deflected" in event["shot"]:
                    out["bool5"] = event["shot"]["deflected"]
                if "technique" in event["shot"]:
                    out["id1"] = event["shot"]["technique"]["id"]
                if "body_part" in event["shot"]:
                    out["id2"] = event["shot"]["body_part"]["id"]
                if "type" in event["shot"]:
                    out["id3"] = event["shot"]["type"]["id"]
                if "outcome" in event["shot"]:
                    out["id4"] = event["shot"]["outcome"]["id"]
        
        case 19:
            if "substitution" in event:
                if "replacement" in event["substitution"]:
                    out["id1"] = event["substitution"]["replacement"]["id"]
                if "outcome" in event["substitution"]:
                    out["id2"] = event["substitution"]["outcome"]["id"]
        
        case _:
            return out
    return out
                        



three_sixty_data = []
freeze_frames = []
def loadThreeSixtyFileData(threeSixtyDirectory, usedMatchIds):
    frame_id_count = 0
    for root, dirs, files in os.walk(threeSixtyDirectory):
        for filename in files:
            fullPath = os.path.join(root, filename)
            splitPath = fullPath.split("\\")
            matchId = splitPath[-1].split(".")[0]
            print("Now Reading:" + str(fullPath))
            if matchId in usedMatchIds:
                # manually map the values into new dictionaries/json objects and insert those into the database
                currfile = open(fullPath, encoding="utf8")
                threeSixtyDataList = json.load(currfile)
                currfile.close()

                for threeSixtyEntry in threeSixtyDataList:
                    curr360 = {"event_uuid": threeSixtyEntry["event_uuid"],
                            "match_id": matchId,
                            "visible_area": threeSixtyEntry["visible_area"]}
                    curr_freeze_frame_ids = []

                    for frame in threeSixtyEntry["freeze_frame"]:
                        curr_frame = {"frame_id": frame_id_count}
                        
                        if "location" in frame:
                            curr_frame["frame_location"] = frame["location"]

                        if "teammate" in frame:
                            curr_frame["teammate"] = frame["teammate"]

                        if "actor" in frame:
                            curr_frame["actor"] = frame["actor"]

                        if "keeper" in frame:
                            curr_frame["keeper"] = frame["keeper"]

                        freeze_frames.append(curr_frame)
                        curr_freeze_frame_ids.append(frame_id_count)
                        frame_id_count += 1
                    curr360["freeze_frame"] = curr_freeze_frame_ids
                    three_sixty_data.append(curr360)


lineups = []
players = []
positions = []
def loadLineupsFileData(lineupsDirectory, usedMatchIds):
    for root, dirs, files in os.walk(lineupsDirectory):
        for filename in files:
            fullPath = os.path.join(root, filename)
            splitPath = fullPath.split("\\")
            matchId = splitPath[-1].split(".")[0]
            print("Now Reading:" + str(fullPath))

            if matchId in usedMatchIds:
                # manually map the values into new dictionaries/json objects and insert those into the database
                currfile = open(fullPath, encoding="utf8")
                lineupsList = json.load(currfile)
                currfile.close()

                for lineup in lineupsList:
                    lineup_players = []

                    for lineup_item in lineup["lineup"]:
                        lineup_players.append(lineup_item["player_id"])
                        
                        new_player = {"player_id": lineup_item["player_id"],
                                "player_name": lineup_item["player_name"],
                                "jersey_number": lineup_item["jersey_number"]}

                        if "country" in lineup_item:
                            new_player["country_id"] = lineup_item["country"]["id"]
                        if "player_nickname" in lineup_item:
                            new_player["player_nickname"] = lineup_item["player_nickname"]
                        players.append(new_player)

                        for position in lineup_item["positions"]:
                            new_position = {"player_id": lineup_item["player_id"],
                                            "match_id": matchId,
                                            "position_id": position["position_id"],
                                            "position_name": position["position"],
                                            "position_to": position["to"],
                                            "position_from": position["from"],
                                            "to_period": position["to_period"],
                                            "from_period": position["from_period"],
                                            "start_reason": position["start_reason"],
                                            "end_reason": position["end_reason"]}
                            positions.append(new_position)

                    new_lineup = {"team_id": lineup["team_id"],
                                    "match_id": matchId,
                                    "lineup": lineup_players}
                    
                    lineups.append(new_lineup)


usedCompetitionIds = loadCompetitionFileData(competitionsFile)
usedMatchIds = loadMatchFileData(matchesDirectory, usedCompetitionIds)
files_loaded = loadEventFileData(eventsDirectory, usedMatchIds)

loadThreeSixtyFileData(threeSixtyDirectory, usedMatchIds)
loadLineupsFileData(lineupsDirectory, usedMatchIds)

populateFreezeFrames(freeze_frames)
populateCountries(countries)
populateStadiums(stadiums)
loadTacticsFromTempFiles(files_loaded)
populateSeasons(seasons)
populatePlayers(players)
populateManagers(managers)
populateCompetitions(competitions)
populateReferees(referees)
populateTeams(teams)
populateMatches(matches)
populateLineups(lineups)
loadEventsFromTempFiles(files_loaded)
populatePositions(positions)
populateThreeSixtyData(three_sixty_data)
loadTypedEventsFromTempFiles(files_loaded)



