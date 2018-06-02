include RecommendationBot::Analyzers

describe TriggerAnalyzer do
  let(:whitelist) { ['lorem', 'ipsum', 'dolor', 'sit'] }
  let(:blacklist) { ['aap', 'noot', 'mies'] }
  let(:username) { '/u/test_bot' }

  subject do
    list = ListAnalyzer.new(whitelist, blacklist)
    name = ListAnalyzer.new([username], [])
    TriggerAnalyzer.new(list, name)
  end

  it('should return true if a word is whitelisted') do
    message = 'Dummy text usually starts with lorem.'
    result = subject.contains_trigger? message
    expect(result).to be true
  end

  it('should return false if a word is NOT whitelisted') do
    message = 'Dummy text usually starts with a capital letter.'
    result = subject.contains_trigger? message
    expect(result).to be false
  end

  it('should return false if a word is blacklisted') do
    message = 'Dummy text usually starts with "lorem" or "aap".'
    result = subject.contains_trigger? message
    expect(result).to be false
  end

  it('should ignore case') do
    message = 'Dummy text usually starts with "lorem" or "AAP".'
    result = subject.contains_trigger? message
    expect(result).to be false
  end

  it('should return true if the username is mentioned') do
    message = "aap noot #{username}"
    result = subject.contains_trigger? message
    expect(result).to be true
  end
end