import datetime
import requests
import json


def ifAvailable(variable, key):
    try:
        return variable[key]
    except Exception as e:
        return None


def getTime(variable, timezone=0):
    try:
        return datetime.datetime.fromtimestamp(variable + timezone).strftime("%H:%M")
    except Exception as e:
        return f"N.A."


def getDate(variable, timezone=0):
    try:
        return datetime.datetime.fromtimestamp(variable + timezone).strftime("%d/%m")
    except Exception as e:
        return f"N.A."

def getDay(variable, timezone=0):
    try:
        return datetime.datetime.fromtimestamp(variable + timezone).strftime("%A")
    except Exception as e:
        return f"N.A."



def getJSON(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
