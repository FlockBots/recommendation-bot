module RecommendationBot
  module Repositories
  end
end

%w(submission_sqlite)
  .each { |file| require_relative File.join('repositories', file) }
