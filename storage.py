import json
import glob
import os
import re
import datetime

class Storage:

 
    def save(filename, data):
        with open(filename, 'w') as file:  
            json.dump(data, file, ensure_ascii=False)

    def load(filename):
        with open(filename) as file:  
            data = json.load(file)
        return data

    def check_files_exists():
        files = glob.glob('storage/post*')
        if not files:
            return False
        return True 

    def last_file():
        files = glob.glob('storage/post*')
        latest = max(files, key=os.path.getctime)
        return latest

    def last_history_file():
        files = glob.glob('storage/history_post*')
        latest = max(files, key=os.path.getctime)
        return latest

    def load_last_file():
        file = Storage.last_file()
        return Storage.load(file)

    def load_history_file():
        file = Storage.last_history_file()
        return Storage.load(file)

    def get_date(filename):
        regex = r"(\d{4})-(\d{2})-(\d{2})"
        matches = re.search(regex, filename)
        date = datetime.datetime.strptime(matches.group(), '%Y-%m-%d')
        return date