include RecommendationBot::Analyzers

describe ListAnalyzer do
  let(:whitelist) { ['lorem', 'ipsum', 'dolor', 'sit'] }
  let(:blacklist) { ['aap', 'noot', 'mies'] }

  subject do
    ListAnalyzer.new(whitelist, blacklist)
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
end
