include RecommendationBot::Data

describe Data do
  describe '#read_list' do
    it 'reads the line of a file' do
      lines = ['foo', 'bar', 'baz']
      expect(File).to receive(:readlines).and_return(lines)

      result = RecommendationBot::Data.read_list('test_data')
      expect(result).to eq lines
    end

    it 'removes empty lines' do
      lines = ['foo', 'bar', "\t", "\n", "\r\n", '', 'baz']
      expect(File).to receive(:readlines).and_return(lines)

      result = RecommendationBot::Data.read_list('test_data')
      expect(result).to eq ['foo', 'bar', 'baz']
    end
  end
  
  describe '#read_template' do
    it 'reads a file' do
      content = 'lorem ipsum dolor sit amet'
      expect(File).to receive(:read).and_return content
      result = RecommendationBot::Data.read_template('test_template')
      expect(result).to eq content
    end
  end
end
