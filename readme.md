# Recommendation Bot

This is a Reddit bot written for /u/Razzafrachen. By default, the bot monitors /r/Bourbon, /r/Scotch and /r/Whiskey for submissions that ask for suggestions for what whisky to buy.
It does so by comparing the title and text of a submission to a list of keywords. If any of the keywords appear in them, it replies a premade message tailored for that subreddit.

The keywords and replies are stored in `recommendationbot/data/`. Each reply is stored in `{subreddit}.md` where `{subreddit}` is the name of the subreddit in lowercase. In `all.md` is the reply the bot will send if it replies in any other subreddit.

## Installation
The bot is built on Python 3 and depends on a few external modules. These modules can be installed using `pip install -R requirements.txt`.
The configuration of the bot is inside `recommendationbot/config`. Any `.ini` file will be recognised as a potential configuration. In case of multiple configurations, the script will ask which one to use at start-up.
If a configuration is not completed (i.e. some of the required keys are empty), the script will guide the user through the configuration steps. But it is also possible to copy `template.ini` to a new file and fill it in manually.

A few important configuration keys are the following:

* clientid
The client id is a unique identifier provided by Reddit. It can be found on https://www.reddit.com/prefs/apps/ > developed applications. Then under the title of the application is a string with random characters. That is the client id.
* clientsecret
The client secret is a similar identifier and found in the same place. When you edit the developed application Reddit, it shows the value as the first item (**secret**).
* redirecturi
This is the URI where Reddit redirects the user to after authentication. The only important thing to know is that this should be the same as filled in in the Reddit preferences (under apps > developed applications).
* refreshtoken
This a token received from the Reddit server after authentication. This should be left empty as it is filled in automatically by the script.

## Improvements / To do
* Move database operations to separate file
* Send reply on 'paging'.
* Send general reply if not from any of the monitored subs.
