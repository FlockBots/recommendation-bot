include RecommendationBot::Repositories

require_relative '../support/mock_api'

describe SqliteLastSeenRepository do
  let(:db) { ':memory:' }
  let(:subreddit) { MockSubreddit.new('flockbots') }
  let(:submission) { MockSubmission.new('1', subreddit, 'selftext', Time.now, true) }

  subject do
    described_class.new(db)
  end

  it('should raise when storing the same ID twice') do
    subject.store(subreddit.display_name, submission)
    expect { subject.store('something else', submission) } .to raise_error(SQLite3::ConstraintException)
  end

  it('should raise when fetching a subreddit that is not stored') do
    expect { subject.fetch('nothing') }.to raise_error(KeyError)
  end

  it('should return the default value if subreddit cannot be found') do
    default = 'can be anything'
    expect(subject.fetch('nothing', default)).to eq default
  end

  it('should retrieve the newest submission') do
    older_submission = MockSubmission.new('2', subreddit, 'some text', Time.now - 60)
    subject.store(subreddit.display_name, older_submission)
    subject.store(subreddit.display_name, submission)

    result = {
      id: submission.id,
      replied_to: submission.replied_to?
    }
    expect(subject.fetch(subreddit.display_name)).to eq result
  end

  it('should retrieve the id and replied_to flag') do
    subject.store(subreddit.display_name, submission)
    result = {
      id: submission.id,
      replied_to: submission.replied_to?
    }
    expect(subject.fetch(subreddit.display_name)).to eq result
  end
end