require 'sqlite3'

module RecommendationBot::Repositories
  class SqliteLastSeenRepository
    def initialize(database)
      @db = SQLite3::Database.new database
      create_table_if_not_exists
    end

    def fetch(subreddit, default = nil)
      query = 'SELECT id FROM lastseen WHERE subreddit = ? ORDER BY created_at DESC LIMIT 1'
      result = @db.execute(query, [subreddit])
      return default if result.empty?
      result.first.first # single result, single value
    end

    def store(subreddit, submission)
      query = 'INSERT INTO lastseen VALUES (?, ?, ?)'
      date_string = submission.created_at.strftime('%Y%m%d%H%M')
      @db.execute(query, [submission.id, subreddit.downcase, date_string]);
    end

    private

    def create_table_if_not_exists
      query = <<-SQL.strip
        CREATE TABLE IF NOT EXISTS lastseen (
          id TEXT UNIQUE,
          subreddit TEXT,
          created_at INTEGER
        )
      SQL
      @db.execute(query)
    end
  end
end
