require_relative './hash_like_behaviour'

include RecommendationBot::Repositories

describe SqliteSubmissionRepository do
  let(:db) { ':memory:' }
  let(:id) { 'lovely_liskov' }

  subject do
    SqliteSubmissionRepository.new(db)
  end

  it_should_behave_like 'a hash'

  it('should raise when storing the same ID twice') do
    subject.store id
    expect { subject.store id } .to raise_error(SQLite3::ConstraintException)
  end

  it('stored ids can be retrieved') do
    subject.store id
    expect(subject.fetch id).to eq [id]
  end
end