import json

def read_token(filename):
    with open(filename,'r',encoding="utf8") as json_file:
        data = json.load(json_file)
        return data["token"]

def read_bad(filename):
    with open(filename,'r',encoding="utf8") as json_file:
        data = json.load(json_file)
        return data["bad"]