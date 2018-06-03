module RecommendationBot::Data
  def self.read_list(filename)
    lines = File.readlines(filename)
    lines.map(&:strip).reject(&:empty?)
  end

  def self.read_template(filename)
    File.read(filename).strip
  end
end