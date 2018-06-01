include RecommendationBot::Repositories

require_relative '../support/mock_api'

describe SqliteLastSeenRepository do
  let(:db) { ':memory:' }
  let(:subreddit) { MockSubreddit.new('flockbots') }
  let(:submission) { MockSubmission.new('1', subreddit, 'selftext', Time.now) }

  subject do
    described_class.new(db)
  end

  it('throw when storing the same ID twice') do
    subject.store(subreddit.display_name, submission)
    expect { subject.store('something else', submission) } .to raise_error(SQLite3::ConstraintException)
  end

  it('should retrieve the newest submission') do
    older_submission = MockSubmission.new('2', subreddit, 'some text', Time.new(2017))
    subject.store(subreddit.display_name, older_submission)
    subject.store(subreddit.display_name, submission)

    expect(subject.fetch(subreddit.display_name)).to eq submission.id
  end
end