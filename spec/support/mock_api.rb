MockSubreddit = Struct.new(:display_name)
MockMessage = Struct.new(:subreddit, :body) do
  def mark_as_read
    nil
  end
end
MockSubmission = Struct.new(:id, :subreddit, :selftext, :created_at, :replied) do
  def self?
    selftext != nil
  end

  def replied_to?
    replied
  end
end


class MockApi
  def initialize(output)
    @output = output
  end
  def username
    'test_bot'
  end

  def reply(post, message)
    @output << message
    nil
  end

  def submissions(subreddit, before: nil)
    subreddit = MockSubreddit.new('Scotch')
    [
      MockSubmission.new('1', subreddit, nil),
      MockSubmission.new('2', subreddit, 'blacklisted keyword'),
      MockSubmission.new('3', subreddit, 'whitelisted keyword')
    ]
  end

  def inbox(before: nil)
    subreddit = MockSubreddit.new('Scotch')
    [
      MockMessage.new(subreddit, 'whitelisted keyword'),
      MockMessage.new(subreddit, 'blacklisted keyword')
    ]
  end
end