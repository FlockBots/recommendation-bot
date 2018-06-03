MockSubreddit = Struct.new(:display_name)
MockMessage = Struct.new(:body, :link) do
  def mark_as_read
    nil
  end

  def subreddit
    link.subreddit
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
  def initialize(output, subreddit, submissions, messages)
    @output = output
    @subreddit = subreddit
    @submissions = submissions
    @messages = messages
  end
  def username
    'test_bot'
  end

  def reply(post, message)
    @output << message
    nil
  end

  def submissions(subreddit, before: nil)
    @submissions
  end

  def inbox(before: nil)
    @messages
  end
end