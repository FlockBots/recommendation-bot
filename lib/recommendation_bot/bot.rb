module RecommendationBot
  class Bot

    def initialize(analyzer, api, submissions, templates)
      @analyzer = analyzer
      @api = api
      @submissions = submissions
      @templates = templates
    end

    def check_inbox
      @api.inbox.each do |message|
        if @analyzer.contains_trigger? message.body
          reply_to message
          message.mark_as_read
        end
      end
    end

    def check_subreddits(*subreddits)
      subreddits.each do |sub|
        before = @submissions.last_seen(sub, nil)
        submissions = @api.submissions(sub, before: before)
        check_submissions(submissions)
      end
    end

    private

    def reply_to(post)
      return if replied_to?(post)
      # clone the template otherwise altering the
      # message will change the original template
      message = @templates.fetch(post.subreddit.display_name.downcase).clone
      @api.reply(post, message)
      # convert from comment to submission
      # TODO: Extract method?
      if post.respond_to? :link
        post = post.link
      end
      @submissions.store(post)
    end

    def replied_to?(post)
      # convert from comment to submission
      # TODO: Extract method?
      if post.respond_to? :link
        post = post.link
      end
      stored_submission = @submissions.fetch(post.id, false)
      stored_submission && stored_submission[:replied_to]
    end

    def check_submissions(submissions)
      submissions.each do |submission|
        if !submission.self?
          next
        end
        if @analyzer.contains_trigger? submission.selftext
          reply_to submission
        end
      end
    end
  end
end
