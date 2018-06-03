require_relative '../support/mock_api'

include RecommendationBot::Repositories

describe SqliteSubmissionRepository do
  let(:db) { ':memory:' }
  let(:id) { 'lovely_liskov' }
  
  let(:subreddit) { MockSubreddit.new('flockbots') }
  let(:submission) { MockSubmission.new('1', subreddit, 'selftext', Time.now, false) }

  subject do
    SqliteSubmissionRepository.new(db)
  end
  
  describe('#store') do
    it('should update if the id already exists') do
      subject.store(submission)
      submission.replied = !submission.replied
      subject.store(submission)
      result = subject.fetch(submission.id)
      expect(result[:replied_to]).to be submission.replied
    end
  end

  describe('#fetch') do
    it('should retrieve the id and replied_to flag') do
      subject.store(submission)
      date = submission.created_at
      result = {
        id: submission.id,
        subreddit: submission.subreddit.display_name.downcase,
        replied_to: submission.replied_to?,
        created_at: DateTime.new(date.year, date.month, date.day, date.hour, date.min)
      }
      expect(subject.fetch(submission.id)).to eq result
    end
    
    context('when the key cannot be found') do
      it('should raise an error') do
        expect { subject.fetch('nothing') }.to raise_error(KeyError)
      end
    
      it('should return the default value if specified') do
        default = 'can be anything'
        expect(subject.fetch('nothing', default)).to eq default
      end
    end
  end

  describe('#last_seen') do
    it('should return the most recent submission from the subreddit') do
      older_submission = MockSubmission.new('2', subreddit, 'selftext', Time.now - 60, false)
      subject.store(older_submission)
      subject.store(submission)
      result = subject.last_seen(subreddit.display_name)
      expect(result[:id]).to eq submission.id
    end

    context('when the subreddit cannot be found') do
      it('should raise an error') do
        expect { subject.last_seen('nothing') }.to raise_error(KeyError)
      end
  
      it('should return the default value if specified') do
        result = subject.last_seen('nothing', 'default value')
        expect(result).to eq result
      end
    end

  end
end