### What?

[@wearebasefm](http://www.twitter.com/wearebasefm) is a twitter bot which crawls [@wearebase](http://www.twitter.com/wearebase)'s Last.fm feed every minute and compares the latest track with what we have on record. If it's new, it's tweeted.

### Why?

[Base Creative Agency](http://www.basecreativeagency.com) listens to a lot of music during the day, and I thought it would be fun to share our musical tastes.

### How?

- [@wearebase](http://www.twitter.com/wearebase) uses iTunes to scrobble music with Last.fm.
- Every minute, the [crontab](https://github.com/picklepete/wearebasefm/blob/master/cron/crontab.txt) kicks in and parses Last.fm's 'recent tracks' feed.
- The script then compares when the last track was played (if at all, it may well be the first time), and if this track has been played since, it's tweeted.
- The message is then inserted into the database, so in just under a minute's time, we can determine whether any new tracks have been played.

### Prerequisites:

1. [tweepy](https://github.com/joshthecoder/tweepy) - an python library for the Twitter API.
2. [MySQLdb](http://sourceforge.net/projects/mysql-python) - a python MySQL db API.
3. [feedparser](http://www.feedparser.org) - a python based RSS & Atom feed parser.

### Installation:

First of all, ensure your `apt-get` list is up-to-date by performing a `sudo apt-get update`.

Next, change the username in the Twadio arg to your Last.fm username, seen here:

`twadio = Twadio(username='wearebase')`

#### Installing tweepy:

1. `cd` into your `src` directory, such as `~/src`.
2. `git clone git://github.com/joshthecoder/tweepy.git && cd tweepy`
3. `python setup.py install && sudo python setup.py install`

#### Installing MySQLdb:

1. `sudo apt-get install python-mysqldb`
2. `mysql -uroot -p` and create our database.
3. `mysql -uroot -p DATABASE_NAME < sql/schema_20110318.sql`

#### Installing feedparser

1. Return to your `src` directory.
2. `svn checkout http://feedparser.googlecode.com/svn/trunk/ feedparser && cd feedparser`
3. `python setup.py build && sudo python setup.py install`

#### Installing the crontab

1. `crontab -e`
2. Paste the crontab line, you may need to change the path to the python file.
3. Write and exit, if you are in Vim, use `:wq`. You can verify it's saved via `crontab -l`.