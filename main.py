from parsing import *
from plotter import *

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