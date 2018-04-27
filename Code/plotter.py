import json as json
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets
from matplotlib import ticker
import networkx as nx
from pandas import DataFrame

class Plotter:

    def pieChart(self, tweets, retweets, replies):
        total = tweets + retweets + replies
        # The slices will be ordered and plotted counter-clockwise.
        percents = [(float(tweets)/float(total)*100.0), (float(retweets)/float(total)*100.0),(float(replies)/float(total)*100.0)]

        labels = 'Tweets (' + str(percents[0]) + '%)', 'Retweets (' + str(percents[1]) + '%)', 'Replies (' + str(percents[2]) + '%)'
        fracs = [tweets, retweets, replies]
        colors = ['#ff4d4d', '#0FAC36', '#0F18AC'] # red, green, blue

        patches, texts = plt.pie(fracs, colors=colors, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')

        plt.tight_layout()
        plt.title('Pie Chart Showing Frequencies of Different Activity Types')
        plt.show()

    def barChart(self, tweets, retweets, replies):
        vals = [tweets, retweets, replies]
        labels = ('Tweets', 'Retweets', 'Replies')
        n_groups = len(vals)
        bar_width = 1/1.5
        pos = np.arange(len(labels))
        
        plt.bar(pos, vals, align='center', alpha=0.5)
        plt.xticks(pos, labels)
        plt.ylabel('Absolute Frequency')
        plt.xlabel('Activity Type')
        plt.title('Bar Chart Showing Frequencies of Different Activity Types')

        plt.show()

        # fig.set_xlabel('Activity')
        # fig.set_ylabel('Frequency (absolute)')
        # fig.set_title('Comparing absolute frequencies of activities')
        # fig.set_xticks(n_groups + bar_width)
        # fig.set_xticklabels(('Tweets', 'Retweets', 'Replies'))
        # fig.legend()

        # fig.tight_layout()
        # plt.show()

    def tweetsTimeLine(self, data):
        tweets = data[data['text'].str.startswith("RT") == False]
        groupbytime = tweets.groupby('time').count()
        time = groupbytime.iloc[:, 0]
        count = 0
        num = [] #number of tweets
        xticks = []
        for i, v in time.iteritems():
            count += 1
            num.append(v)
            xticks.append(i)

        y = num
        fig, ax = plt.subplots()
        ax.plot(y)
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 300))
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        ax.set_xticklabels(xticks, rotation='vertical', fontsize=8)
        ax.set_xlabel('Time and Date')
        ax.set_ylabel('Number of Tweets')
        plt.show()

    def retweetsTimeLine(self, data):
        retweets = data[data['text'].str.startswith("RT") == True]
        groupbytime = retweets.groupby('time').count()
        time = groupbytime.iloc[:, 0]
        count = 0
        num = [] #number of tweets
        xticks = []
        for i, v in time.iteritems():
            count += 1
            num.append(v)
            xticks.append(i)

        y = num
        fig, ax = plt.subplots()
        ax.plot(y)
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 300))
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        ax.set_xticklabels(xticks, rotation='vertical', fontsize=8)
        ax.set_xlabel('Time and Date')
        ax.set_ylabel('Number of Retweets')
        plt.show()
        
    def repliesTimeLine(self, data):
        replies = data[data['in_reply_to_screen_name'].notnull() == True]
        groupbytime = replies.groupby('time').count()
        time = groupbytime.iloc[:, 0]
        count = 0
        num = [] #number of tweets
        xticks = []
        for i, v in time.iteritems():
            count += 1
            num.append(v)
            xticks.append(i)

        y = num
        fig, ax = plt.subplots()
        ax.plot(y)
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 300))
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        ax.set_xticklabels(xticks, rotation='vertical', fontsize=8)
        ax.set_xlabel('Time and Date')
        ax.set_ylabel('Number of Replies')
        plt.show()
        
    def hashTagesWordCloud(self, data):
        hashTags = data.loc[:, 'entities_str']
        words = []
        for i, v in hashTags.items():
            try:
                j = json.loads(v)
                for tag in j['hashtags']:
                    if tag['text'] != "CometLanding":
                        words.append(tag['text'])
            except TypeError:
                pass

        wordcloud = WordCloud(width=1000, height=500).generate(" ".join(words))
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
    
    def repliesToTwoUsers(self, data):
        interactions = []
        for index, row in data.iterrows():
            sentBy = row['from_user']
            inReplyTo = row['in_reply_to_screen_name']
            if sentBy == None or inReplyTo == None or type(sentBy) != str or type(inReplyTo) != str: continue
            interactions.append([sentBy, inReplyTo])
        return DataFrame(interactions).drop_duplicates()

    def retweetsToTwoUsers(self, data):
        interactions = []
        for index, row in data.iterrows():
            sentBy = row['from_user']
            tweetText = row['text']

            if sentBy == None or tweetText == None or type(tweetText) != str or type(sentBy) != str: continue
            splitText = tweetText.split()
            if len(splitText) < 2: continue
            
            retweeting = splitText[1].replace(":", "").replace("@", "")
            interactions.append([sentBy, retweeting])

        return DataFrame(interactions).drop_duplicates()

    def mentionsToTwoUsers(self, data):
        interactions = []
        for index, row in data.iterrows():
            sentBy = row['from_user']
            tweetText = row['text']

            if sentBy == None or tweetText == None or type(tweetText) != str or type(sentBy) != str: continue
            splitText = tweetText.split()
            if len(splitText) < 1: continue
            else:
                for string in splitText:
                    if (string.startswith("@")):
                        interactions.append([sentBy, string])

        return DataFrame(interactions).drop_duplicates()
    
    def networkGraph(self, plotItemList, whatPlotting):
        G = nx.DiGraph()

        print("Now drawing the graph showing all " + whatPlotting + " between users.")

        if (whatPlotting == "interactions"): plotItemList = DataFrame(plotItemList)

        for index, row in plotItemList.iterrows():
            G.add_edge(row[0], row[1])
        UG = G.to_undirected()

        width = 0.003
        if (whatPlotting == "replies"): width = 0.4
        if (whatPlotting == "mentions"): width = 0.07

        options = {
            'node_color': 'black',
            'node_size': 1,
            'line_color': 'grey',
            'linewidths': 0,
            'width': width,
        }

        nx.draw_circular(UG, **options)
        plt.show()
        print("Graph density = " + str(nx.density(G))) # TODO: print some more properties of the graph
        if (whatPlotting != "interactions" and whatPlotting != "mentions"): print("\n\n")

    def interactionsPieChart(self, retweets, replies, mentions):
        total = retweets + replies + mentions
        # The slices will be ordered and plotted counter-clockwise.
        percents = [(float(retweets)/float(total)*100.0), (float(replies)/float(total)*100.0),(float(mentions)/float(total)*100.0)]

        labels = 'Retweets (' + str(percents[0]) + '%)', 'Replies (' + str(percents[1]) + '%)', 'Mentions (' + str(percents[2]) + '%)'
        fracs = [retweets, replies, mentions]
        colors = ['#ff4d4d', '#0FAC36', '#0F18AC'] # red, green, blue

        patches, texts = plt.pie(fracs, colors=colors, shadow=True, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')

        plt.tight_layout()
        plt.title('Pie Chart Showing Frequencies of Different Interaction Types')
        plt.show()
