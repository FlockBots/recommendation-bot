require 'dotenv'
require 'redd'

include RecommendationBot

describe RedditApi do
  let(:session) do
    Dotenv.load 'test.env'
    Redd.it(
      user_agent: ENV.fetch('RB_USER_AGENT'),
      client_id:  ENV.fetch('RB_CLIENT_ID'),
      secret:     ENV.fetch('RB_SECRET'),
      username:   ENV.fetch('RB_USERNAME'),
      password:   ENV.fetch('RB_PASSWORD'),
      max_retries: ENV.fetch('RB_RETRIES', 0)
    )
  end

  subject do
    RedditApi.new(session)
  end

  it('should retrieve the username') do
    expect(subject.username).to eq 'recommendation_bot'
  end

  it('should retrieve the latest submissions of a subreddit') do
    submissions = subject.submissions('scotch')
    counter = 0
    submissions.each do |submission|
      counter += 1
      expect(submission.subreddit.display_name).to eq 'Scotch'
      break
    end
    expect(counter).to be 1
  end

  it('should retrieve submissions after a specified submission') do
    submissions = subject.submissions('scotch')
    counter = 0
    id = nil
    date = nil
    submissions.each do |submission|
      counter += 1
      if counter == 5
        id = submission.name
        date = submission.created_at
        break
      end
    end

    new_submissions = subject.submissions('scotch', before: id)
    counter = 0
    new_submissions.each do |submission|
      counter += 1
      expect(submission.created_at).to be >= date
    end
    expect(counter).to be > 0
  end

  it('should not throw errors when retrieving unread messages') do
    expect { subject.inbox }.not_to raise_error
    expect(subject.inbox).to_not be_nil
  end
end