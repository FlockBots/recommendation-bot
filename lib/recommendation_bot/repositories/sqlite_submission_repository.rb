require 'sqlite3'

module RecommendationBot::Repositories
  class SqliteSubmissionRepository
    def initialize(database)
      @db = SQLite3::Database.new database
      create_table_if_not_exists
    end

    def fetch(id, default = nil)
      query = 'SELECT id, replied_to FROM submissions WHERE id = ?'
      records = @db.execute(query, [id])
      if records.empty?
        return default || raise(KeyError, "key not found: '#{id}'")
      end
      convert records.first
    end
    
    def last_seen(subreddit, default = nil)
      query = 'SELECT id, replied_to FROM submissions WHERE subreddit = ? ORDER BY created_at DESC LIMIT 1'
      records = @db.execute(query, [subreddit.downcase])
      if records.empty?
        return default || raise(KeyError, "subreddit not found: '#{subreddit}'")
      end
      convert records.first
    end

    def store(submission)
      query = 'INSERT OR REPLACE INTO submissions VALUES (?, ?, ?, ?)'
      date_string = submission.created_at.strftime('%Y%m%d%H%M')
      replied = submission.replied_to? ? 1 : 0
      subreddit = submission.subreddit.display_name
      @db.execute(query, [submission.id, subreddit.downcase, date_string, replied]);
    end

    private

    def convert(record)
      result = {
        id: record[0],
        replied_to: record[1] == 1
      }
    end

    def create_table_if_not_exists
      query = <<-SQL.strip
        CREATE TABLE IF NOT EXISTS submissions (
          id TEXT UNIQUE,
          subreddit TEXT,
          created_at INTEGER,
          replied_to INTEGER
        )
      SQL
      @db.execute(query)
    end
  end
end
