import praw
import sqlite3
import os
import logging
import time
import requests
from recommendationbot.config import authorize
from recommendationbot.database import VisitedDatabase
from recommendationbot import data

def set_logging(config):
    logging.basicConfig(
        filename=config['LOGGING']['File'],
        format='{name:^8} | {asctime} | {levelname:^8} | {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{',
        level=int(config['LOGGING']['Level'])
    )
    requests_logger = logging.getLogger('requests')
    prawcore_logger = logging.getLogger('prawcore')
    requests_logger.setLevel(logging.ERROR)
    prawcore_logger.setLevel(logging.ERROR)

def find_config(extension='.ini'):
    path = os.path.join('recommendationbot', 'config')
    configs = []
    for fname in os.listdir(path):
        if fname.endswith(extension):
            configs.append(fname)
    if len(configs) == 0:
        return 'config'
    elif len(configs) == 1:
        return configs[0]
    else:
        conf_list = ', '.join([config[:-len(extension)] for config in configs])
        print('Multiple configurations found, please choose one:')
        print(conf_list)
        config = input('Configuration: ')
        chosen = config + extension in configs
        while not chosen:
            print('')
            print('Unknown configuration, please choose on from the list below.')
            print(conf_list)  
            config = input('Configuration: ')
            chosen = config + extension in configs
        return config

def run():
    config_name = find_config()
    reddit, config = authorize.connect(config_name)
    set_logging(config)
    if reddit == None:
        logging.error("Authorization failure.")
        return
    logging.info('Starting bot as /u/{user} using the "{config}" configuration.'.format(
        user=reddit.user.me(),
        config=config_name
    ))
    db = db_connect(config)
    bot = RecommendationBot(reddit, config, db)
    subreddits = get_subreddits(config)
    print('Scanning subreddits...')
    while True:
        try:
            bot.check_subreddits(subreddits)
        except requests.exceptions.ConnectionError:
            logging.error("Connection Failure. Waiting 5 minutes before retrying.")                  
            time.sleep(300)
        except Exception as e:
            db.close()
            logging.exception('Unexpected error')
            raise e

def selftest():
    reddit, config = authorize.connect('debug')
    if reddit == None:
        print("- Failed to connect...")
    else:
        print("+ Connected to Reddit using {}'s account".format(reddit.user.me()))
    bot = RecommendationBot(reddit, config)
    subreddits = get_subreddits(config)
    print('+ Subreddits: {}'.format(', '.join(subreddits)))
    replies = bot.load_replies(subreddits)
    keywords = bot.load_keywords()
    print('+ Replies and keywords located in "{}"'.format(config['BOT']['DataLocation']))
    print("! Self test completed")

def get_subreddits(config):
    return [s.strip() for s in config['BOT']['Subreddits'].split(',')]

class RecommendationBot:
    def __init__(self, reddit, config):
        self.reddit = reddit
        self.config = config
        self.db = VisitedDatabase(config)

    def check_subreddits(self, subreddits):
        assert type(subreddits) is list
        replies  = data.load_replies(subreddits, self.config)
        keywords = data.load_keywords(self.config)
        blacklist = data.load_blacklist(self.config)

        multireddit = '+'.join(subreddits)
        subreddit = self.reddit.subreddit(multireddit)

        for submission in subreddit.stream.submissions():
            if self.db.visited(submission): 
                continue
            self.db.visit(submission)

            title = submission.title.lower()
            text  = submission.selftext.lower()
            all_text = '{} {}'.format(title, text)
            
            contains_blacklist = data.contains(all_text, blacklist) 
            contains_keyword = False
            if not contains_blacklist:
                contains_keyword = data.contains(all_text, keywords) 

            if contains_keyword:
                subname = submission.subreddit.display_name
                logging.debug('Replying to {author} in {sub}'.format(
    		    author=submission.author.name,
    		    sub=subname
    	        ))
                try:
                    replyTemplate = replies[subname.lower()]
                except KeyError:
                    if 'all' in replies:
                        replyTemplate = replies['all']
                submission.reply(replyTemplate)

