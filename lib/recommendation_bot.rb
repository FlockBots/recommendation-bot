module RecommendationBot
end

lib_path = File.expand_path('../recommendation_bot', __FILE__)

# commands
# bot
files = %w(
  api
  repositories
).each { |file| require File.join(lib_path, file) }
