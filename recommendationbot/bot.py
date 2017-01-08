import praw
import sqlite3
import os
import logging
import time
import threading
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
    bot = RecommendationBot(reddit, config)
    print('Scanning subreddits...')
    while True:
        try:
            bot.monitor_reddit()
        except ConnectionResetError:
            logging.error("Connection Failure. Waiting 5 minutes before retrying.")                  
            time.sleep(300)
        except praw.exceptions.APIException:
            logging.exception('PRAW Exception')
        except Exception as e:
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
    data_dir = config['BOT']['DataLocation']
    replies = data.load_replies(subreddits, data_dir)
    keywords = data.load_list(data_dir, 'keywords.txt')
    blacklist = data.load_list(data_dir, 'blacklist.txt')
    print('keywords: {}, blacklisted: {}'.format(
        len(replies),
        len(keywords),
        len(blacklist)
    ))
    print('+ Replies, keywords and blacklist located in "{}"'.format(config['BOT']['DataLocation']))
    print("! Self test completed")

def get_subreddits(config):
    return [s.strip() for s in config['BOT']['Subreddits'].split(',')]

class RecommendationBot:
    def __init__(self, reddit, config):
        self.reddit = reddit
        self.config = config
        self.subreddits = get_subreddits(config)
        self.replies  = data.load_replies(self.subreddits, config['BOT']['DataLocation'])

    def monitor_reddit(self):
        subreddit_thread = threading.Thread(target=self.check_subreddits)
        mentions_thread = threading.Thread(target=self.check_mentions)
        mentions_thread.start()
        subreddit_thread.start()
        mentions_thread.join()
        subreddit_thread.join()

    def check_subreddits(self):
        logging.debug('Checking subreddits...')
        db = VisitedDatabase(self.config)
        
        data_dir = self.config['BOT']['DataLocation'] 
        keywords = data.load_list(data_dir, 'keywords.txt')
        blacklist = data.load_list(data_dir, 'blacklist.txt')

        multireddit = '+'.join(self.subreddits)
        subreddit = self.reddit.subreddit(multireddit)
        
        for submission in subreddit.stream.submissions():
            if db.visited(submission): 
                continue
            db.visit(submission)

            title = submission.title.lower()
            text  = submission.selftext.lower()
            all_text = '{} {}'.format(title, text)
            
            blacklisted = data.contains(all_text, blacklist, 'blacklist') 
            contains_keyword = False
            if not blacklisted:
                contains_keyword = data.contains(all_text, keywords, 'keywords') 

            if contains_keyword:
                subname = submission.subreddit.display_name
                logging.debug('(Submission) Replying to {author} in {sub}'.format(
                    author=submission.author.name,
                    sub=subname
                ))
                self.reply(subname, submission)

    def check_mentions(self):
        logging.debug('Checking mentions...')
        db = VisitedDatabase(self.config)
        while True:
            for mention in self.reddit.inbox.mentions():
                if db.visited(mention):
                    continue
                db.visit(mention)
                subname = mention.subreddit.display_name
                logging.debug('(Mention) Replying to {author} in {sub}'.format(
                    author=mention.author.name,
                    sub=subname
                ))
                self.reply(subname, mention)
            time.sleep(60)

    def reply(self, subname, obj):
        try:
            replyTemplate = self.replies[subname.lower()]
        except KeyError:
            if 'all' in self.replies:
                logging.debug('Using general reply template for "/r/{}"'.format(subname))
                replyTemplate = self.replies['all']
            else:
                logging.warn('No reply template provided for subreddit "{}"'.format(subname))
                return
        obj.reply(replyTemplate)
