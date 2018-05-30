require 'sqlite3'

module RecommendationBot::Repositories
  class SubmissionSqliteRepository
    def initialize(database)
      @db = SQLite3::Database.new database
      create_table_if_not_exists
    end

    def get(id)
      query = 'SELECT id FROM submissions WHERE id = ?'
      @db.execute(query, [id])
    end

    def put(id)
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
