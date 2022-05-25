# for disable the uniqe exception we can use INSERT OR IGNORE


# This module provides utility functions to work with the database
# 1. data_exist(id, tablename): returns True if the givin id exsist in the givin tablename.
# 2. get_query(tablename): returns List of the givin tablename.
# 3. create_profile(id, discord_name): returns True if the Profile created else False.
# 4. create_member(id, discord_name, role_id, room_id): returns True if Member is created else returns False.
# 5. create_room(id): returns True if the Room is created, else return False.
# 6. create_message(id, profile_id, room_id, content): returns True Message is created, else return False.
# 7. create_event(id, name, message, target_date): returns True if Event is created, else return False.

import datetime
import sqlite3
import traceback
import pytest
import os

path = 'db.sqlite3'
con = sqlite3.connect(path) # TODO: create connection function
cur = con.cursor()
time_sign = datetime.datetime.now() # # @out - 2022-04-25 11:12:14.148420
cwd = os.getcwd()

print(f"Connected to: {path}\nPath: {cwd}")

def create_rules() -> bool:
    try:
        cur.execute(f"INSERT INTO webapp_roomprofilerole VALUES ('1','Student')")
        cur.execute(f"INSERT INTO webapp_roomprofilerole VALUES ('2','Mentor')")
        cur.execute(f"INSERT INTO webapp_roomprofilerole VALUES ('3','Super Mentor')")
        con.commit()
        return True
    except Exception:
        print(traceback.format_exc())
    return False

def get_query(table_name: str) -> list:
    arr: list = []
    try:
        if(con):
            for row in cur.execute(f'SELECT * FROM {table_name}'):
                arr.append(row)
    except Exception:
        print(traceback.format_exc())
    return arr

def data_exist(id: int, tablename: str) -> bool:
    query: list = get_query(tablename)
    if query != None:
        for data in query:
            if data[0] == id:
                return True
    return False



def create_profile(profile_id: int, discord_name: str) -> bool:
    # create profile will be always part of creating member process.
    # we assuming the connection is exsit. 
    try:
        cur.execute(f"INSERT INTO webapp_profile VALUES ('{profile_id}','{time_sign}','{discord_name}')")
        # we should keep the connection alive so the process keep going.
        return True
    except Exception:
        print(traceback.format_exc())
    return False

def create_member(member_id :int, discord_name: str, role_id: int, room_id: int) -> bool:
    room_table: str = "webapp_room"
    room_exist: bool = data_exist(room_id, room_table)
    profile_id: int = member_id # for us!
    
    try:
        if(con):
            if not room_exist:
                create_room(room_id)
                
            if create_profile(profile_id, discord_name):
                cur.execute(f"INSERT INTO webapp_member VALUES ('{member_id}','{time_sign}','{profile_id}', '{role_id}','{room_id}')")
                con.commit()
                return True
    except Exception:
        print(traceback.format_exc())
    return False

def create_room(room_id: int) -> bool:
    try:
        if(con):
            cur.execute(f"INSERT INTO webapp_room VALUES ('{room_id}','{time_sign}','{time_sign}')")
            con.commit()
            return True
    except Exception:
        print(traceback.format_exc())
    return False

def create_message(message_id: int, profile_id: int, room_id: int, content: str) -> bool:
    room_table: str = "webapp_room"
    profile_table: str = "webapp_profile"

    room_exist: bool = data_exist(room_id, room_table)
    profile_exist: bool = data_exist(profile_id, profile_table)
    
    try:
        if(con):
            if room_exist and profile_exist:
                cur.execute(f"INSERT INTO webapp_message VALUES ('{message_id}','{time_sign}','{content}', '{profile_id}','{room_id}')")
                #FIXME: update_room(room_id)
                con.commit()
                return True
    except Exception:
        print(traceback.format_exc())
    return False

def create_event(event_id: int, name: str, message: str, target_date: str) -> bool:
    # TODO: target_date validation if older then current or other scenarios
    try:
        if(con):
            cur.execute(f"INSERT INTO webapp_event VALUES ('{event_id}','{time_sign}','{name}', '{target_date}','{message}')")
            # call to assign_to_room - function
            con.commit()
            return True
    except Exception:
        print(traceback.format_exc())
    return False

def create_summary(summary_id: int, profile_id: int, room_id: int, content: str) -> bool:
    room_table: str = "webapp_room"
    profile_table: str = "webapp_profile"

    room_exist: bool = data_exist(room_id, room_table)
    profile_exist: bool = data_exist(profile_id, profile_table)
    
    try:
        if(con):
            if room_exist and profile_exist:
                cur.execute(f"INSERT INTO webapp_summary VALUES ('{summary_id}','{time_sign}','{content}','{profile_id}','{room_id}')")
                con.commit()
                return True
            else:
                # TODO: add logic to insure the existence of profile_id and room_id of throw an error about it?
                print(f"one or more of the parameters didnt exist, room_exist: {room_exist}, profile_exist: {profile_exist}")
                return True
    except Exception:
        print(traceback.format_exc())
    return False

############## not done ##############

def assign_to_room(event_id:int ,rooms: list) -> bool:
    try:
        if(con):
            for room_id in rooms:
                # room_id => will be an int => rooms struct as rooms = [1,2,3,4] when values is room id's
                cur.execute(f"INSERT INTO webapp_event_rooms VALUES ('{id}','{event_id}',)")
            con.commit()
            return True
    except Exception:
        print(traceback.format_exc())
    return False



def update_room(room_id: int) -> bool:
    try:
        if(con):
            con.execute(f"UPDATE webapp_room set 'updated_at' = {time_sign} where 'id' = {room_id}")
            return True
    except Exception:
        print(traceback.format_exc())
    return False


# TODO: how we are going to assign the event to the room? room_id? maybe a list of room_ids?
