from customtkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

import time_counter
import os

app = CTk()
app.geometry("320x420+1000+400")
app.title("Game Launcher")
app.resizable(False, False)

set_appearance_mode(mode_string='light')
set_default_color_theme("resource/Sweetkind.json")

main_frame = CTkFrame(master=app, width=300, height=300, fg_color='#F0F8FF', border_color='#7FFFD4')
main_frame.pack_propagate(0)
main_frame.pack(expand=True, padx=(10, 0), pady=(10, 0), anchor='nw')

second_frame = CTkFrame(master=app, width=300, height=100, fg_color='#e6f3ff', border_color='#7FFFD4')
second_frame.pack_propagate(0)
second_frame.pack(side='bottom', padx=(10, 0), pady=(5, 10), anchor='nw')

# Глобальная переменная для хранения пути к .exe файлу
exe_path = ""
total_time = 0


def update_total_time(cursor, game_name):
    game_id = time_counter.find_game_id(cursor=cursor, game_name=game_name)
    total_time = time_counter.get_total_time(cursor=cursor, game_id=game_id)
    tt = round(total_time, 2)
    label_time.configure(text= str(tt) + ' hours')

def browse_path():
    global exe_path
    exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    if exe_path:
        entry.delete(0, "end")
        entry.insert(0, exe_path)


def launch_game():
    global total_time
    if exe_path:
        try:
            db_name = 'time.db'
            connect, cursor = time_counter.connect_to_db(db_name)
            time_counter.create_table(connect, cursor)

            game_name = os.path.basename(exe_path)
            time_counter.launch_game_and_track_time(exe_path, connect, cursor, game_name)
            update_total_time(cursor=cursor, game_name=game_name)
            print(f"Игра {game_name} успешно запущена и время учтено.")

        except Exception as e:
            print(f"Ошибка при запуске игры: {e}")

btn_browse = CTkButton(master=main_frame, text='Выберите .exe файл', 
                       fg_color="transparent", hover_color='#72788D', 
                       border_color='#191919', border_width=3, 
                       text_color='#191919', text_color_disabled="#000000",
                       command=browse_path)
btn_browse.pack(anchor='w', padx=(50, 50), pady=(25,0))

entry = CTkEntry(master=main_frame, placeholder_text="Путь к .exe файлу", width=200, 
                 fg_color="transparent", border_color="#191919", 
                 border_width=2, text_color='#191919')
entry.pack(anchor='w', padx=(50, 50), pady=(25, 0))

btn_launch = CTkButton(master=main_frame, text='Запустить игру', 
                       fg_color="transparent", hover_color='#72788D', 
                       border_color='#191919', border_width=3,
                       text_color='#191919',
                       command=launch_game)
btn_launch.pack(anchor='w', padx=(50, 50), pady=(25,0))


label_time = CTkLabel(master=second_frame, text=total_time,
                      text_color='#191919')
label_time.pack(anchor='w', padx=(10, 10), pady=(25,0))

app.mainloop()
