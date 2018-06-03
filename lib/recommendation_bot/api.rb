module RecommendationBot
  class RedditApi
    def initialize(client)
      @client = client
      @username = nil
    end

    def username
      return @username unless @username.nil?
      @username = @client.me.name
    end

    def reply(post, message)
      post.reply(message)
    end

    def submissions(subreddit, before: nil)
      options = { before: before }
      submissions = @client.subreddit(subreddit).new(options)
      if before.nil?
        return submissions
      else
        # TODO: Fix this upstream
        thing = @client.from_ids(before)
        date = thing.first.created_at
        return Enumerator.new do |results|
          submissions.each do |submission|
            if submission.created_at < date
              break
            end
            results << submission
          end
        end
      end
    end

    def inbox(before: nil)
      options = { category: 'unread', mark: false }
      options = options.merge(before: before) unless before.nil?
      @client.my_messages(options)
    end
  end
end