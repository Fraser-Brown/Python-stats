from parsing import *
from plotter import *

cr = CensusReader("data/CometLanding.csv")
retweets = cr.retweetCount()
replys = cr.replyCount()
tweets = cr.tweetCount()

# print("retweets:")
# print(retweets)
# print("replys:")
# print(replys)
# print("tweets:")
# print(tweets)
# print("Number of Users:")
# cr.numOfUsers()
# cr.mostPopHashtags()

plotter = Plotter()
# plotter.tweetsTimeLine(cr.data)
# plotter.structurePlot(tweets, retweets, replys)
plotter.hashTagesWordCloud(cr.data)
