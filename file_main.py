import os
import json


def createFolder(name):
    if os.path.isdir(name):
        os.rmdir(name)
    if os.path.isfile(name):
        os.remove(name)
    open(name, 'a').close()


def writeData(data):
    with open('managerud.dta', 'w', encoding='utf-8') as d:
        json.dump(data, d, ensure_ascii=False)


def defaultData():
    data = {
        "user_select_dont_show": False,
        "user_color_mode": "light"
    }
    return data


def getData():
    try:
        with open('managerud.dta', 'r') as f:
            data = json.load(f)
            return data
    except:
        createFolder("managerud.dta")
        writeData(defaultData())
        return False


def getProp(prop):
    user_data = getData()
    if user_data:
        if prop in user_data:
            return user_data[prop]
        else:
            writeData(defaultData())
            return 2
    return 2


def writeProp(prop, data):
    user_data = getData()
    if user_data:
        if prop in user_data:
            user_data[prop] = data
            writeData(user_data)
            return True
        else:
            writeData(defaultData())
            return False
    return False
