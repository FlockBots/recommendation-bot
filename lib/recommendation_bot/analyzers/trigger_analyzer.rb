module RecommendationBot::Analyzers
  # This class should only combine other analyzers
  class TriggerAnalyzer
    def initialize(list_analyzer, username_analyzer)
      @list_analyzer = list_analyzer
      @username_analyzer = username_analyzer
    end

    def contains_trigger?(text)
      lowercase_text = text.downcase
      whitelisted = @list_analyzer.contains_trigger? lowercase_text
      contains_username = @username_analyzer.contains_trigger? lowercase_text

      whitelisted || contains_username
    end
  end
end