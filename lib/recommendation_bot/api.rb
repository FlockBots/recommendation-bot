module RecommendationBot
  class RedditApi
    def initialize(redd_client)
      @client = client
    end

    def submissions(subreddit, before: nil)
      options = {}
      options = options.merge(before: before) unless before.nil?
      @client.subreddit(subreddit).submissions()
    end

    def inbox(before: nil)
      options = { category: 'unread', mark: false }
      options = options.merge(before: before) unless before.nil?
      @client.messages(options)
    end
  end
end