import sqlite3
import os

class VisitedDatabase:

    DB_NAME = 'submissions.db'
    TABLE = 'visited_submissions'

    def __init__(self, config):
        self.config = config
        self.connection = self.connect(config)
    
    def create_database(self, path):
        db = sqlite3.connect(path)
        c = db.cursor()
        c.execute('CREATE TABLE visited_submissions (submission_id text)')
        db.commit()
        db.close()

    def connect(self, config):
        db_path = os.path.join(config['BOT']['DataLocation'], 'visited.db')
        if not os.path.exists(db_path):
            self.create_database(db_path)
        return sqlite3.connect(db_path)

    def visit(self, submission):
        if self.visited(submission):
            return
        c = self.connection.cursor()
        c.execute('INSERT INTO {} (submission_id) VALUES (?)'.format(VisitedDatabase.TABLE), [submission.fullname])
        self.connection.commit()

    def visited(self, submission):
        c = self.connection.cursor()
        c.execute('SELECT * FROM {} WHERE submission_id = ?'.format(VisitedDatabase.TABLE), [submission.fullname])
        return c.fetchone()
