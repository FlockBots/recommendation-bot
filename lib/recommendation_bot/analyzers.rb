module RecommendationBot
  module Analyzers
  end
end

%w(
  list_analyzer
  trigger_analyzer
).each { |file| require_relative File.join('analyzers', file) }
