module RecommendationBot
  module Repositories
  end
end

%w(
  sqlite_submission_repository
)
  .each { |file| require_relative File.join('repositories', file) }
