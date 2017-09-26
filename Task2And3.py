import glob
import json
import os
import sqlite3

import pandas as pd

DATA_BASE_NAME = 'all_posts_results.sqlite'
conn = sqlite3.connect(DATA_BASE_NAME)

def task2():
    folderList = glob.glob('*s')
    for folder in folderList:
        file_list = os.listdir(folder)
        print("Current folder " + folder)
        for file in file_list:
            current_file = folder + "//" + file
            with open(current_file, encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                data_frame = pd.io.json.json_normalize(data)
                data_frame.to_sql(folder, conn, if_exists='append')


def task3():
    result3_1 = pd.read_sql('SELECT albumId, count(id) AS photo_count '
                            'FROM photos GROUP BY albumId', conn)

    result3_2 = pd.read_sql('SELECT albums.userId AS userId, count(photos.id) AS photo_count '
                            'FROM photos '
                            'INNER JOIN albums ON photos.albumId = albums.id '
                            'GROUP BY userId', conn)

    result3_3 = pd.read_sql('SELECT  users.id AS userID, users.name, count(photos.id) AS photo_count '
                            'FROM photos '
                            'INNER JOIN albums ON photos.albumId = albums.id '
                            'INNER JOIN users ON albums.userId = users.id '
                            'GROUP BY userId', conn)
    print(result3_1)
    print(result3_2)
    print(result3_3)
