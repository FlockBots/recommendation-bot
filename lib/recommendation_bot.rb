module RecommendationBot
end

lib_path = File.expand_path('../recommendation_bot', __FILE__)

files = %w(
  data
  bot
  api
  repositories
  analyzers
).each { |file| require File.join(lib_path, file) }
