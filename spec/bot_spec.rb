require_relative './support/mock_api'
include RecommendationBot
include RecommendationBot::Analyzers

describe Bot do
  let(:output) { [] }
  let(:api) do
    subreddit = MockSubreddit.new('Scotch')
    subs = [
      MockSubmission.new('1', subreddit, nil),
      MockSubmission.new('2', subreddit, 'blacklisted keyword'),
      MockSubmission.new('3', subreddit, 'whitelisted keyword')
    ]
    messages = [
      MockMessage.new('whitelisted keyword', subs.first),
      MockMessage.new('blacklisted keyword', subs.first)
    ]
    MockApi.new(output, subreddit, subs, messages)
  end
  let(:templates) { { 'scotch' => 'foo bar scotch template' } }
  let(:submissions) do
    data = {}
    submissions = double('repository')
    allow(submissions).to receive(:fetch) { |*args| data.fetch(*args) }
    allow(submissions).to receive(:store) do |submission|
      data.store(submission.id, submission)
    end
    submissions
  end

  subject do
    analyzer = ListAnalyzer.new(['whitelisted', 'keyword'], ['blacklist'])
    allow(submissions).to receive(:last_seen).and_return('1')
    Bot.new(analyzer, api, submissions, templates)
  end
  
    describe('#check_inbox') do
      it('stores the last seen submission') do
        expect(submissions).to receive(:store)
        subject.check_inbox
      end
      
      it('checks messages in its inbox for triggers') do
        original = templates['scotch'].clone # check for side-effects
        subject.check_inbox
        expect(output).to eq [original]
      end
    end

  describe('#check_subreddits') do
    it('stores the last seen submission') do
      expect(submissions).to receive(:store)
      subject.check_subreddits('scotch')
    end

    it('checks submissions in subreddits for triggers') do
      original = templates['scotch'].clone # check for side-effects
      subject.check_subreddits('scotch')
      expect(output).to eq [original]
    end
  end
end