import os
import logging

def load_replies(subreddits, config, extension='.md'):
    path = os.path.join(config['BOT']['DataLocation'], 'all' + extension)
    if not os.path.exists(path):
        logging.warn('Bot cannot reply outside configurated subreddits without "{}"'
                .format('all' + extension)
        )
    files = map(str.lower, subreddits)
    replies = {}
    for name in files:
        path = os.path.join(config['BOT']['DataLocation'], name + extension)
        with open(path, 'r') as replyFile:
            replies[name] = replyFile.read()
    return replies

def load_keywords(config, filename='keywords.txt'):
    path = os.path.join(config['BOT']['DataLocation'], filename)
    keywords = []
    with open(path, 'r') as keywordFile:
        keywords = keywordFile.readlines()
    return keywords

def load_blacklist(config, filename='blacklist.txt'):
    path = os.path.join(config['BOT']['DataLocation'], filename)
    keywords = []
    with open(path, 'r') as keywordFile:
        keywords = keywordFile.readlines()
    return keywords

def contains(text, words):
    text = text.lower()
    for word in words:
        word = word.strip().lower()
        if word in text:
            logging.debug('Text contains: {}'.format(word))
            return True
