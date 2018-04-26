from parsing import *
from plotter import *
from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

cr = CensusReader("data/CometLanding.csv")
retweets = cr.retweetCount()
replies = cr.replyCount()
tweets = cr.tweetCount()

# print("retweets:")
# print(retweets)
# print("replies:")
# print(replies)
# print("tweets:")
# print(tweets)
# print("Number of Users:")
# cr.numOfUsers()
# cr.mostPopHashtags()

plotter = Plotter()
# plotter.tweetsTimeLine(cr.data)
# plotter.structurePlot(tweets, retweets, replies)
plotter.hashTagesWordCloud(cr.data)