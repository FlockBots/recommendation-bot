import praw, webbrowser, os
from configparser import ConfigParser

def main():
    botconfig = ConfigParser()
    configfile = 'config/config.ini'
    botconfig.read(configfile)
    redditConfig = botconfig['REDDIT']
    reddit = praw.Reddit(
        user_agent=redditConfig['UserAgent'],
        client_id=redditConfig['ClientId'],
        client_secret=redditConfig['ClientSecret'],
        redirect_uri=redditConfig['RedirectUri']
    )
    state = 'AnyKindOfGibberishWillDo'
    scopes = ['submit', 'privatemessages', 'identity']
    url = reddit.auth.url(scopes, state, 'permanent')
        
    webbrowser.open(url)
    print('The browser just opened a window. Please press the `Allow` button on Reddit')
    print('Then copy the string behind `code=` in the URL bar and paste it below')
    code = input('Authorization code: code=') 
    
    redditConfig['RefreshToken'] = reddit.auth.authorize(code)
    with open(configfile, 'w') as cfile:
        botconfig.write(cfile)
    print('Authorization succeeded for user `{}`!'.format(reddit.user.me()))

if __name__ == '__main__':
    main()
