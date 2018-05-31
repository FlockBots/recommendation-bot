module RecommendationBot
  class ListAnalyzer
    def initialize(whitelist, blacklist)
      @whitelist = whitelist
      @blacklist = blacklist
    end

    def contains_trigger?(text)
      lowercase = text.downcase
      contained_in?(lowercase, @whitelist) && !contained_in?(lowercase, @blacklist)
    end

    private

    def contained_in?(text, list)
      list.reduce(false) do |memo, word|
        memo || (text.include? word)
      end
    end
  end
end