import os
import logging

def load_replies(subreddits, data_dir, extension='.md'):
    path = os.path.join(data_dir, 'all' + extension)
    if not os.path.exists(path):
        print('Warning: Bot cannot reply outside configurated subreddits without "all{}"'.format(extension))
        logging.warn('Bot cannot reply outside configurated subreddits without "{}"'
                .format('all' + extension)
        )
    else:
        subreddits.append('all')
    files = map(str.lower, subreddits)
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

def contains(text, words):
    text = text.lower()
    for word in words:
        word = word.strip().lower()
        if word in text:
            logging.debug('Text contains: {}'.format(word))
            return True
    return False
