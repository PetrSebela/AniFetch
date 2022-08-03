from bs4 import BeautifulSoup
from requests import request
import json
import display
from rich import print

ANIMELIST = 'https://myanimelist.net/profile/'
config = {}

decoration = {
    'underline': lambda length: "-"* length,
    'space': ''
}


data = {
    'User': { },
    'Anime': {},
    'Manga': {}
}

logo = []
logoWidth = 0

def loadConfig(path):
    global config
    try:
        with open(path) as configFile:
            fileContent = configFile.read()
            config = json.loads(fileContent)
            data['User']['Username']= config['username']
        return True
    except:
        return False


def fetchData(username):
    global data

    page = request('get', ANIMELIST + username)        
    soup = BeautifulSoup(page.content, 'html.parser')

    if page.status_code == 404:
        print("> User not found try changing username in config.json")
        return False

    prefix = 'Anime'
    for index, stat in enumerate(soup.find_all(class_='clearfix mb12')):
        entry = list(stat.find_all('span'))
        if(index == 8):
            prefix = 'Manga'
        if(len(entry) == 2):
            data[prefix][entry[0].get_text()] = entry[1].get_text()
        if(len(entry) == 1):
            data[prefix][stat.find('a').get_text()] = entry[0].get_text()
    return True


def showStats(display):
    for statIndex, stat in enumerate(config['stats']):
        if stat['category'] == 'Decoration':
            if stat['name'] == 'space':
                continue

            if stat['name'] == 'tag':
                display.addString(text=stat['value'],
                                  x=logoWidth + config['xOffset'],
                                  y=config['yOffset'] + statIndex,
                                  color=stat['style'])

        else:
            display.addString(text=stat['name'],
                              x=logoWidth + config['xOffset'],
                              y=config['yOffset'] + statIndex,
                              color=stat['headerStyle'])

            display.addString(text=": " + str(data[stat['category']][stat['name']]),
                              x=logoWidth + config['xOffset'] +
                              len(stat['name']),
                              y=config['yOffset'] + statIndex,
                              color=stat['valueStyle'])


if __name__ == "__main__":
    if loadConfig('config.json') and fetchData(config['username']):
        print(data)
        frame = display.frame('fit',
                            border=True,
                            borderSpacingX=config['borderSpacingX'],
                            borderSpacingY=config['borderSpacingY'])

        if config['showLogo']:
            with open(config['logo']['path']) as file:
                logo = file.read().splitlines()
                logoWidth = len(max(logo, key=len))
                frame.addAsciiArt(logo,
                                y=config['logo']['y'],
                                style=config['logo']['style'])

        showStats(display=frame)
        frame.show(config['clearOnLaunch'],
                config['tag'])
