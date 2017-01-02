import praw, webbrowser, os
from configparser import ConfigParser
from recommendationbot.config import configure

BASE_PATH = os.path.join('recommendationbot', 'config')

def getConfig(config='config'):
    path = os.path.join(BASE_PATH, config + '.ini')
    config = ConfigParser()
    config.read(path)
    return config, path

def saveConfig(config, path):
    with open(path, 'w') as configFile:
        config.write(configFile)

def authorize(cname):
    botconfig, path = getConfig(cname)
    redditConfig = botconfig['REDDIT']
    reddit = praw.Reddit(
        user_agent=redditConfig['UserAgent'],
        client_id=redditConfig['ClientId'],
        client_secret=redditConfig['ClientSecret'],
        redirect_uri=redditConfig['RedirectUri']
    )
    state = 'AnyKindOfGibberishWillDo'
    scopes = ['submit', 'identity', 'read']
    url = reddit.auth.url(scopes, state, 'permanent')
        
    webbrowser.open(url)
    print('The browser just opened a window. Please press the `Allow` button on Reddit')
    print('Then copy the string behind `code=` in the URL bar and paste it below')
    code = input('Authorization code: code=') 
    
    redditConfig['RefreshToken'] = reddit.auth.authorize(code)
    saveConfig(botconfig, path)
    print('Authorization succeeded for user `{}`!'.format(reddit.user.me()))

def connect(cname='config'):
    path = os.path.join(BASE_PATH, cname + '.ini')
    if not os.path.exists(path):
        print("No configuration file found in `{}`.".format(path))
        print("Please set up the configuration and try again.")
        configure.configure(cname)

    botconfig, _ = getConfig(cname)
    redditConfig = botconfig['REDDIT']
    if redditConfig['UserAgent'].strip() == '':
        print("Cannot connect to reddit without a UserAgent.")
        print("Please (re)configure and try again.")
        configure.configure(cname)
        return (None, botconfig)
    if redditConfig['ClientId'].strip() == '':
        print("Cannot connect to reddit without a Client ID.")
        print("Please (re)configure and try again.")
        configure.configure(cname)
        return (None, botconfig)
    if redditConfig['ClientSecret'].strip() == '':
        print("Cannot connect to reddit without a Client Secret.")
        print("Please (re)configure and try again.")
        configure.configure(cname)
        return (None, botconfig)
    if redditConfig['RefreshToken'].strip() == '':
        if redditConfig['RedirectUri'].strip() == '':
            print("Cannot authorize via reddit without a RedirectUri.")
            print("Please (re)configure and try again.")
            configure.configure(cname)
            return (None, botconfig)
        print("User did not authorize access yet.")
        authorize(cname)
        botconfig, _ = getConfig(cname)
        redditConfig = botconfig['REDDIT']

    reddit = praw.Reddit(
        user_agent=redditConfig['UserAgent'],
        client_id=redditConfig['ClientId'],
        client_secret=redditConfig['ClientSecret'],
        refresh_token=redditConfig['RefreshToken']
    )
    return (reddit, botconfig)

if __name__ == '__main__':
    authorize()
