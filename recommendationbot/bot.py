import praw
import sqlite3
import os
import logging
import time
import requests
from recommendationbot.config import authorize

def db_create(path):
    db = sqlite3.connect(path)
    c = db.cursor()
    c.execute('CREATE TABLE visited_submissions (submission_id text)')
    db.commit()
    db.close()

def db_connect(config):
    db_path = os.path.join(config['BOT']['DataLocation'], 'visited.db')
    if not os.path.exists(db_path):
        db_create(db_path)
    return sqlite3.connect(db_path)

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

def visit(submission, db):
    if visited(submission, db):
        return
    c = db.cursor()
    c.execute('INSERT INTO visited_submissions (submission_id) VALUES (?)', [submission.fullname])
    db.commit()

def visited(submission, db):
    c = db.cursor()
    c.execute('SELECT * FROM visited_submissions WHERE submission_id = ?', [submission.fullname])
    return c.fetchone()

class RecommendationBot:
    def __init__(self, reddit, config, db):
        self.reddit = reddit
        self.config = config
        self.db = db

    def check_subreddits(self, subreddits):
        assert type(subreddits) is list
        multireddit = '+'.join(subreddits)
        subreddit = self.reddit.subreddit(multireddit)
        replies  = self.load_replies(subreddits)
        keywords = self.load_keywords()
        for submission in subreddit.stream.submissions():
            if visited(submission, self.db): 
                continue
            visit(submission, self.db)
            title = submission.title.lower()
            text  = submission.selftext.lower()
            logging.debug('Analyzing submission {}'.format(submission.url))
            containsKeyword = False
            for keyword in keywords:
                keyword = keyword.strip().lower()
                if keyword in title or keyword in text:
                    containsKeyword = True
                    break
            if containsKeyword:
                subname = submission.subreddit.display_name
                logging.debug('Replying to {author} in {sub}'.format(
    		    author=submission.author.name,
    		    sub=subname
    	        ))
                replyTemplate = replies[subname.lower()]
                submission.reply(replyTemplate)

    def load_replies(self, subreddits, extension='.md'):
        files = map(str.lower, subreddits)
        replies = {}
        for name in files:
            path = os.path.join(self.config['BOT']['DataLocation'], name + extension)
            with open(path, 'r') as replyFile:
                replies[name] = replyFile.read()
        return replies

    def load_keywords(self, filename='keywords.txt'):
        path = os.path.join(self.config['BOT']['DataLocation'], filename)
        keywords = []
        with open(path, 'r') as keywordFile:
            keywords = keywordFile.readlines()
        return keywords

