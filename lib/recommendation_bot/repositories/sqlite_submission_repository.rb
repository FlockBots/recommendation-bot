require 'sqlite3'

module RecommendationBot::Repositories
  class SqliteSubmissionRepository
    def initialize(database)
      @db = SQLite3::Database.new database
      create_table_if_not_exists
    end

    def fetch(id, default = nil)
      query = 'SELECT id FROM submissions WHERE id = ?'
      records = @db.execute(query, [id])
      if records.empty?
        return default || raise(KeyError, "key not found: '#{id}'")
      end
      return records.first
    end

    def store(id)
      query = 'INSERT INTO submissions VALUES (?)'
      @db.execute(query, [id]);
    end

    private

    def create_table_if_not_exists
      query = <<-SQL.strip
        CREATE TABLE IF NOT EXISTS submissions (id TEXT UNIQUE)
      SQL
      @db.execute(query)
    end
  end
end
