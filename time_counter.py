#import psutil
import time
import subprocess as sp
import sqlite3
import string
import os
import logging

from datetime import datetime, timedelta

#
#           DATA BASE
#
def connect_to_db(db_name : string):
    try: 
        connect = sqlite3.connect(db_name)
        return connect, connect.cursor()
    except:
        logging.warn(f"connection to {db_name} failed")
        logging.critical(f"exiting...")
        quit() 


# create new table in database
def create_table(connect : sqlite3.Connection, cursor : sqlite3.Cursor):

    try:
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS `session` (
            `game_id` integer,
            `started_at` integer,
            `ended_at` integer
            );''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS `games` (
            `id` integer,
            `name` text,
            `total_hours` real,
            `created_at` integer
            );''')
        
        print('table is created')

        connect.commit()

        logging.debug("db is create")

    except: logging.warn('Error to create db!')

 
# register new session
def commit_session(connect : sqlite3.Connection, cursor : sqlite3.Cursor, game_id, launch_time, commit_time):
    try:
        cursor.execute(f'''
        INSERT INTO session
        VALUES (
            {game_id},
            {launch_time},
            {commit_time}         
        )''')

        connect.commit()

        logging.debug("session is commit")
    except: 
        print(f"Error to commit_session")


# get game list
def get_game_list(connect: sqlite3.Connection, cursor : sqlite3.Cursor):
    game_list = cursor.execute('SELECT name FROM games')
    return game_list.fetchall()


# register new game w/ intecremented id
def commit_game(connect : sqlite3.Connection, cursor : sqlite3.Cursor, game_name):  
    #get game_id  
    try:
        game_id = cursor.execute('SELECT id FROM games ORDER BY id DESC LIMIT 0, 1;')
        game_id = game_id.fetchone()
        game_id = game_id[0] + 1

    except: 
        game_id = 0


    game_exist = True


    if not game_exist:
        try: 
            cursor.execute(f'''INSERT INTO games 
                            VALUES (
                            {game_id},
                            '{game_name}',
                            0,
                            '{int(datetime.now().timestamp())}');
                            ''')

            connect.commit()

        except:
            logging.warn('Error to commit game')


# get value from session
def get_sessions(cur : sqlite3.Cursor, row, game_id):
    try: 
        if game_id != -1:
            result = cur.execute(f'''
                        SELECT {row} FROM session
                        WHERE game_id = {game_id};
                        ''')
        else:
            result = cur.execute(f'''
                        SELECT {row} FROM session;
                        ''')
        
        return result.fetchall()
    
    except:
        logging.warn('Error to get sessions')


# update game time
def update_game_time(connect : sqlite3.Connection, cursor : sqlite3.Cursor, game_id):
    total_seconds = all_time_count(cursor, game_id)

    hours = total_seconds/3600      

    try: 
        cursor.execute(f'''
                    UPDATE games
                    SET total_hours = {hours}   
                    WHERE id = {game_id};
                    ''')
        
        connect.commit()

    except:
        logging.warn('Error to update game time')
#
#           TIME LOGIC
#
def all_time_count(cur : sqlite3.Cursor, game_id : int):
    if game_id != -1:
        sessions = get_sessions(cur, '*', game_id)

    else:
        sessions = get_sessions(cur, '*', 0)


    seconds_count = 0


    for i in range(len(sessions)):
        # sessions is array : sessions[id][1-startime/2-endtime]   
        # where session[id][1/2] is datetime.timestamp

        time_difference = sessions[i][2] - sessions[i][1]

        seconds_count += time_difference 

    return seconds_count
          

# if __name__ == "__main__":

#     run = True

#     path_to_exe = r'C:\Windows\system32\notepad.exe'

#     # connect to db and create tables
    
#     connect, cursor = connect_to_db('time.db')

#     create_table(connect=connect, cursor=cursor)  

#     # register new game   
#     commit_game(connect=connect, cursor=cursor, game_name='Valorant')

#     # start counter        

#     try:
#         launch_time = datetime.now().timestamp()
#         sp.run(path_to_exe)
#         end_time = datetime.now().timestamp()
        
#     except:
#         print(f"Error to launch {path_to_exe}")

    
#     commit_session(cursor=cursor, connect=connect ,launch_time=launch_time, commit_time=end_time, game_id=0)
    
#     update_game_time(connect=connect, cursor=cursor, game_id=0)
    
