include RecommendationBot::Repositories

describe SubmissionSqliteRepository do
  let(:db) { ':memory:' }
  let(:id) { 'lovely_liskov' }

  subject do
    SubmissionSqliteRepository.new(db)
  end

  it('throw when storing the same ID twice') do
    subject.put id
    expect { subject.put id } .to raise_error(SQLite3::ConstraintException)
  end

  it('stored ids can be retrieved') do
    expect(subject.get id).to eq []
    subject.put id
    expect(subject.get id).to eq [[id]]
  end
end