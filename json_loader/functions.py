import psycopg2
import json
from config import load_config

def populateMatches(dataBlob):
    sql = """ INSERT INTO matches
               SELECT * FROM json_populate_recordset(NULL::matches, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateCountries(dataBlob):
    sql = """ INSERT INTO countries
               SELECT * FROM json_populate_recordset(NULL::countries, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateTeams(dataBlob):
    sql = """ INSERT INTO teams
               SELECT * FROM json_populate_recordset(NULL::teams, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateManagers(dataBlob):
    sql = """ INSERT INTO managers
               SELECT * FROM json_populate_recordset(NULL::managers, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateReferees(dataBlob):
    sql = """ INSERT INTO referees
               SELECT * FROM json_populate_recordset(NULL::referees, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateSeasons(dataBlob):
    sql = """ INSERT INTO seasons
               SELECT * FROM json_populate_recordset(NULL::seasons, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateStadiums(dataBlob):
    sql = """ INSERT INTO stadiums
               SELECT * FROM json_populate_recordset(NULL::stadiums, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))





def populateEvents(dataBlob):
    sql = """ INSERT INTO events
               SELECT * FROM json_populate_recordset(NULL::events, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateTactics(dataBlob):
    sql = """ INSERT INTO tactics
               SELECT * FROM json_populate_recordset(NULL::tactics, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateTypedEvents(dataBlob):
    sql = """ INSERT INTO typed_events
               SELECT * FROM json_populate_recordset(NULL::typed_events, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))





def populateCompetitions(dataBlob):
    sql = """ INSERT INTO competitions
               SELECT * FROM json_populate_recordset(NULL::competitions, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))






def populateThreeSixtyData(dataBlob):
    sql = """ INSERT INTO data360
               SELECT * FROM json_populate_recordset(NULL::data360, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populateFreezeFrames(dataBlob):
    sql = """ INSERT INTO freeze_frames
               SELECT * FROM json_populate_recordset(NULL::freeze_frames, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))





def populateLineups(dataBlob):
    sql = """ INSERT INTO lineups
               SELECT * FROM json_populate_recordset(NULL::lineups, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populatePlayers(dataBlob):
    sql = """ INSERT INTO players
               SELECT * FROM json_populate_recordset(NULL::players, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))

def populatePositions(dataBlob):
    sql = """ INSERT INTO positions
               SELECT * FROM json_populate_recordset(NULL::positions, %s)  
               ON CONFLICT DO NOTHING;"""
    connectAndExecute(sql, (json.dumps(dataBlob),))


def connectAndExecute(sql, args):
    #performs common action of connecting to poatgres and executing the sql passed in
    config = load_config()

    try:
        with  psycopg2.connect(**config) as connection:
            with  connection.cursor() as cursor:
                # execute the statement passed as an argument
                cursor.execute(sql, args)

                # commit the changes to the database
                connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)          

def connectAndExecuteJson(sql, args, jsonArgs):
    #performs common action of connecting to poatgres and executing the sql passed in
    config = load_config()

    try:
        with  psycopg2.connect(**config) as connection:
            with  connection.cursor() as cursor:
                # execute the statement passed as an argument
                cursor.execute(sql, (args, json.dumps(jsonArgs),))

                # commit the changes to the database
                connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)          