from configparser import ConfigParser
from getpass import getpass
import os
import logging

def main():
    print('* * * Recommendation Bot Configuration * * *')
    filename = input('Configuration name (default: config): ')
    if filename.strip() == '':
        filename = 'config'
    filename = filename.lower() + '.ini'
    configpath = os.path.join('config', filename)
    if os.path.exists(configpath):
        print('A configuration with the name `{}` already exists.'.format(filename))
        contPrompt = input('Do you want to modify this configuration? [y/n]')
        if contPrompt.lower() == 'n':
            print('Exiting configuration setup')
            return
        config = loadConfiguration(configpath)
    else:
        config = createDefaultConfiguration()

    config = promptConfig(config)
    with open(configpath, 'w') as configfile:
        config.write(configfile)
    print('Configuration complete!')

def loadConfiguration(configpath):
    config = ConfigParser()
    config.read(configpath)
    return config

def createDefaultConfiguration():
    config = ConfigParser()
    config['REDDIT'] = {
        'UserAgent': 'Whisky Recommendation Bot by /u/FlockOnFire and /u/Razzafrachen',
        'ClientId': '',
        'ClientSecret': '',
        'RedirectUri': '',
        'RefreshToken': ''
    }
    config['LOGGING'] = {
        'File': os.path.join('logs', 'bot.log'),
        'Level': logging.INFO,
        # 'Format': '{asctime} | {levelname:^8} | {message}',
        # 'DateFormat': '%Y-%m-%d %H:%M:%S',
        # 'FormatStyle': '{'
    }
    config['BOT'] = {
        'IdleSleepTime': 60,
        'DataLocation': os.path.join('data', '')
    }
    return config

def promptConfig(config):
    for section in config:
        print(' == Section: {} == '.format(section))
        configsection = config[section]
        for key in configsection:
            prompt = ("{} ('{}')\n > ".format(key, configsection[key]))
            configsection[key] = getValue(default=configsection[key], prompt=prompt)
        print('')
    return config

def getValue(default='', prompt='New value (leave empty for default): ', secret=False):
    inp = getpass if secret else input
    value = inp(prompt).strip()
    return default if value == '' else value

if __name__ == '__main__':
    main()

