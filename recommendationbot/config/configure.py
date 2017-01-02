from configparser import ConfigParser
from getpass import getpass
import os
import logging

def configure(name='config'):
    print('* * * Recommendation Bot Configuration * * *')
    filename = input('Configuration name (default: {}): '.format(name))
    if filename.strip() == '':
        filename = name
    filename = filename.lower() + '.ini'
    configpath = os.path.join('recommendationbot', 'config', filename)
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
    return (config, name)

def loadConfiguration(configpath):
    config = ConfigParser()
    config.read(configpath)
    return config

def createDefaultConfiguration():
    config = ConfigParser()
    base_path = 'recommendationbot'
    config['REDDIT'] = {
        'UserAgent': 'Whisky Recommendation Bot by /u/FlockOnFire and /u/Razzafrachen',
        'ClientId': '',
        'ClientSecret': '',
        'RedirectUri': '',
        'RefreshToken': ''
    }
    config['LOGGING'] = {
        'File': os.path.join(base_path, 'logs', 'bot.log'),
        'Level': logging.INFO,
        # 'Format': '{asctime} | {levelname:^8} | {message}',
        # 'DateFormat': '%Y-%m-%d %H:%M:%S',
        # 'FormatStyle': '{'
    }
    config['BOT'] = {
        'DataLocation': os.path.join(base_path, 'data', ''),
        'Subreddits': 'Bourbon,Scotch,Whiskey'
    }
    return config

def promptConfig(config):
    descriptions = {}
    descriptions['REDDIT'] = {
        'useragent': 'Description of the script sent to the Reddit Servers.',
        'clientid': 'Unique identifier for this script as shown in the preferences on Reddit.',
        'clientsecret': 'Secret key for this script as shown in the preferences on Reddit.',
        'redirecturi': 'URI to redirect to in authorization process as filled in in the preferences on Reddit.',
        'refreshtoken': '(Filled in automatically if empty) Access token as provided by the Reddit OAuth process. '
    }
    descriptions['LOGGING'] = {
        'file': 'File to save the logs to.',
        'level': 'Only show messages of this level and up. ({}) Debug, ({}) Info, ({}) Warning, ({}) Error.'.format(logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR)
    }
    descriptions['BOT'] = {
        'datalocation': 'Directory of any data files.',
        'subreddits': 'subreddits to monitor (comma separated).'
    }
    for section in config:
        print(' == Section: {} == '.format(section))
        configsection = config[section]
        for key in configsection:
            prompt = ("{} ('{}')\n{}\n > ".format(key, configsection[key], descriptions[section][key]))
            configsection[key] = getValue(default=configsection[key], prompt=prompt)
        print('')
    return config

def getValue(default='', prompt='New value (leave empty for default): ', secret=False):
    inp = getpass if secret else input
    value = inp(prompt).strip()
    return default if value == '' else value

if __name__ == '__main__':
    configure()

