import os
import logging

def load_replies(subreddits, data_dir, extension='.md'):
    reply_subs = [sub for sub in subreddits]
    path = os.path.join(data_dir, 'all' + extension)
    if not os.path.exists(path):
        print('Warning: Bot cannot reply outside configurated subreddits without "all{}"'.format(extension))
        logging.warn('Bot cannot reply outside configurated subreddits without "{}"'
                .format('all' + extension)
        )
    else:
        reply_subs.append('all')
    files = map(str.lower, reply_subs)
    replies = {}
    for name in files:
        path = os.path.join(data_dir, name + extension)
        with open(path, 'r') as replyFile:
            replies[name] = replyFile.read()
    return replies

def load_list(data_dir, filename):
    path = os.path.join(data_dir, filename)
    keywords = []
    with open(path, 'r') as keywordFile:
        keywords = keywordFile.read().split()
    return keywords

def contains(text, words, name):
    text = text.lower()
    for word in words:
        word = word.strip().lower()
        if word in text:
            logging.debug('Text contains: "{}" from {}'.format(word, name))
            return True
    return False
