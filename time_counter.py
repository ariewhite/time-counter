import time
import subprocess as sp
import sqlite3
import os
import logging
from datetime import datetime

# Установка логгирования
log_filename = "log.log"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_filename),
                        logging.StreamHandler()
                    ])



# CONNECT TO DB
def connect_to_db(db_name):
    try:
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()
        logging.info(f"Подключение к базе данных {db_name} успешно установлено.")
        return connect, cursor
    except sqlite3.Error as e:
        logging.critical(f"Не удалось подключиться к базе данных {db_name}: {e}")
        raise


# CREATE TABLES
def create_table(connect, cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS session (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            game_id INTEGER,
                            started_at REAL,
                            ended_at REAL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            total_hours REAL DEFAULT 0,
                            created_at REAL)''')

        connect.commit()
        logging.info("Таблицы созданы или уже существуют.")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при создании таблиц: {e}")
        raise


# COMMIT SESSION
def commit_session(connect, cursor, game_id, launch_time, commit_time):
    try:
        cursor.execute('''INSERT INTO session (game_id, started_at, ended_at)
                          VALUES (?, ?, ?)''', (game_id, launch_time, commit_time))
        connect.commit()
        logging.info(f"Сессия игры с ID {game_id} успешно зарегистрирована.")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при записи сессии: {e}")
        raise


# GET GAME LIST
def get_game_list(cursor):
    try:
        cursor.execute('SELECT id, name FROM games')
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении списка игр: {e}")
        raise


# get game total time
def get_total_time(cursor, game_id):
    try:
        print('id', game_id)
        cursor.execute(f'''select total_hours from games
                       where id = ?''', (game_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return 0

    except sqlite3.Error as e:
        logging.error(f"Ошибка при получение часов в игре: {e}")
        raise


# get game id
def find_game_id(cursor: sqlite3.Cursor, game_name):
    try:
        cursor.execute('''SELECT id FROM games
                        WHERE name = ?''', (game_name,))
        result = cursor.fetchone()
        if result:
            return result[0]
        return None
    except sqlite3.Error as e:
        logging.error(f"Ошибка при поиске id игры: {e}")
        raise

# CREATE NEW GAME
def commit_game(connect, cursor, game_name):
    
    try:
        game_id = find_game_id(cursor=cursor, game_name=game_name)
        if game_id:
            logging.info(f'Игра {game_name} уже существует с id {game_id}')
            return game_id
        else:
            cursor.execute('''INSERT INTO games (name, created_at)
                            VALUES (?, ?)''', (game_name, datetime.now().timestamp()))
            connect.commit()
            game_id = cursor.lastrowid
            logging.info(f"Игра '{game_name}' успешно добавлена с ID {game_id}.")
            return game_id
    except sqlite3.Error as e:
        logging.error(f"Ошибка при добавлении игры: {e}")
        raise


# UPDATE GAME TIME
def update_game_time(connect, cursor, game_id):
    try:
        cursor.execute('''UPDATE games
                          SET total_hours = (SELECT SUM(ended_at - started_at) / 3600 FROM session WHERE game_id = ?)
                          WHERE id = ?''', (game_id, game_id))
        connect.commit()
        logging.info(f"Общее время для игры с ID {game_id} обновлено.")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при обновлении общего времени игры: {e}")
        raise


# START GAME 
def launch_game_and_track_time(exe_path, connect, cursor, game_name):

    try:
        game_id = commit_game(connect, cursor, game_name)
        launch_time = datetime.now().timestamp()

        sp.run(exe_path, check=True)

        end_time = datetime.now().timestamp()

        commit_session(connect, cursor, game_id, launch_time, end_time)
        update_game_time(connect, cursor, game_id)

    except Exception as e:
        logging.error(f"Ошибка при запуске игры {game_name}: {e}")
        raise
