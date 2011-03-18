#!/usr/bin/env python
# encoding: utf-8

import re
import sys
import time
from datetime import datetime
from os import popen
import feedparser
import MySQLdb

import urllib2
from urllib import urlencode, quote

import tweepy
from settings import *

try:
	import json
except ImportError:
	import simplejson as json

__author__ = 'evans.peter@gmail.com (Peter Evans)'

class Twadio:
	def __init__(self, username):
		self.version = 1.0
		self.username = username
		self.format = '"%s" by %s - %s %s'
		self.tags = ['nowplaying', 'basefm']
		
		self.shorten_key = 'AIzaSyCPKCU-GITx70O3Lw9jZB7nPsjU-J6CgFg'
		self.shorten_url = 'https://www.googleapis.com/urlshortener/v1/url'
		
		self.build_url()		
		self.db = MySQLdb.connect(host=SQL_HOST, user=SQL_USER, passwd=SQL_PASS, db=SQL_DB)
		self.cursor = self.db.cursor()
		self.get_last_track()
		
	def build_url(self):
		self.url = 'http://ws.audioscrobbler.com/%s/user/%s/recenttracks.rss' % (
			self.version,
			self.username
		)
		
	def get_last_track(self):
		self.cursor.execute('SELECT UNIX_TIMESTAMP(`played_on`) \
							 FROM `tracks` \
							 ORDER BY `played_on` DESC \
							 LIMIT 1')
		try:
			last = self.cursor.fetchone()
			self.last_play = last[0]
		except:
			self.last_play = 0
			
	def get_short_link(self, long_link):
		header = { "Content-Type": "application/json" }
		params = json.dumps({ 'longUrl': long_link, 'key': self.shorten_key })
        
		request = urllib2.Request(self.shorten_url, params, header)
		response = urllib2.urlopen(request)
		
		shortened = json.loads(response.read())
		return shortened['id']
		
	def get_track_detail(self, text):
		artist = title = ''
		text = text.encode('utf-8')
		matches = re.search(r'(?P<artist>[\w\W]+)\–\s(?P<title>[\w\W]+)', text)
		
		if matches is not None:
			artist = matches.group('artist').strip(' ')
			title = matches.group('title').strip(' ')
		else:
			print 'regex failed for %s' % text
			sys.exit()
		
		return artist, title
	
	def save(self, track):
		rawtitle = track['title']
		artist, title = self.get_track_detail(rawtitle)
		
		link = track['link']
		short_link = self.get_short_link(link)
		
		tags = []
		for tag in self.tags:
			tags += ['#%s' % tag.lower()]
		tags = u' '.join(tags)
		
		play_dt = datetime.fromtimestamp(track['updated'])
		played = play_dt.strftime('%Y-%m-%d %H:%M:%S')
		
		message = self.format % (title, artist, short_link, tags)
		
		title = self.db.escape_string(title)
		artist = self.db.escape_string(artist)
		
		self.tweet(message)
		
		self.cursor.execute("INSERT INTO `tracks` (`artist`, `title`, `played_on`, `link`, `short_link`) \
			   				 VALUES ('%s', '%s', '%s', '%s', '%s')" % (artist, title, played, link, short_link))
	
	def tweet(self, message):
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_access_token(FM_ACCESS_KEY, FM_ACCESS_SECRET)
		api = tweepy.API(auth)
		api.update_status(message)
	
	def run(self):
		tracks = {}
		
		try:
			feed = feedparser.parse(self.url)
			tracks = feed['entries']
		except:
			print 'Unable to find feed for user %s' % self.username
			sys.exit()
		
		if len(tracks) > 0:
			for track in tracks:
				updated = datetime.strptime(track['updated'], '%a, %d %b %Y %H:%M:%S +0000')
				stamp = time.mktime(updated.timetuple())
				
				if stamp > self.last_play:
					track['updated'] = stamp
					self.save(track)

if __name__ == '__main__':
	twadio = Twadio(username='wearebase')
	twadio.run()