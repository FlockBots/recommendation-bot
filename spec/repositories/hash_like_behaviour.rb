shared_examples 'a hash' do
  let(:id) { 'single_santa' }

  it('should raise when fetching a key that is not stored') do
    expect { subject.fetch('nothing') }.to raise_error(KeyError)
  end

  it('should return the default value if the key cannot be found') do
    default = 'can be anything'
    expect(subject.fetch('nothing', default)).to eq default
  end
end