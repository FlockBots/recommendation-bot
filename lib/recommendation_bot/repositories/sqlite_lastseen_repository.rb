require 'sqlite3'

module RecommendationBot::Repositories
  class SqliteLastSeenRepository
    def initialize(database)
      @db = SQLite3::Database.new database
      create_table_if_not_exists
    end

    def fetch(subreddit, default = nil)
      query = 'SELECT id, replied_to FROM lastseen WHERE subreddit = ? ORDER BY created_at DESC LIMIT 1'
      records = @db.execute(query, [subreddit])
      if records.empty?
        return default || raise(KeyError, "key not found: '#{subreddit}'")
      end
      result = {
        id: records.first[0],
        replied_to: records.first[1] == 1
      }
    end

    def store(subreddit, submission)
      query = 'INSERT INTO lastseen VALUES (?, ?, ?, ?)'
      date_string = submission.created_at.strftime('%Y%m%d%H%M')
      replied = submission.replied_to? ? 1 : 0
      @db.execute(query, [submission.id, subreddit.downcase, date_string, replied]);
    end

    private

    def create_table_if_not_exists
      query = <<-SQL.strip
        CREATE TABLE IF NOT EXISTS lastseen (
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
