import json as json
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets
from matplotlib import ticker
import networkx as nx

class Plotter:

    def removeDuplicates(self, seq):
        # Not order preserving
        keys = {}
        for e in seq:
            keys[e] = 1
        return keys.keys()

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
        for interaction in data:
            sentBy = interaction['from_user']
            inReplyTo = interaction['in_reply_to_screen_name']
            interactions.append([sentBy, inReplyTo])
        return self.removeDuplicates(sorted(interactions, reverse=False))

    def retweetsToTwoUsers(self, data):
        interactions = []
        for interaction in data:
            sentBy = interaction['from_user']
            inReplyTo = interaction['entities_str']['user_mentions'][0]['screen_name']
            interactions.append([sentBy, inReplyTo])
        return self.removeDuplicates(sorted(interactions, reverse=False))
    
    def getInteractionUsers(self, data):
        # given list of tweets
        # return list of interactions as 2d array
        # each item contains the 2 users involved in the interaction
        replies = data[data['in_reply_to_screen_name'].notnull() == True]
        retweets = data[data['text'].str.startswith("RT") == True]
        formattedRetweets = self.retweetsToTwoUsers(sorted(retweets, reverse=False))
        formattedReplies = self.repliesToTwoUsers(sorted(replies, reverse=False))
        return self.removeDuplicates(sorted(formattedReplies + formattedRetweets, reverse=False))
    
    def networkGraph(self, data):
        # draw each user as a node, each interaction as an edge; eliminate non-interacting users
        print("I'm a graph lol\n\n")
        G = nx.DiGraph()
        interactionUsers = self.getInteractionUsers(data)

        for twoUsers in interactionUsers:
            G.add_edge(twoUsers[0], twoUsers[1])
        UG = G.to_undirected()

        options = {
            'node_color': 'black',
            'node_size': 1,
            'line_color': 'grey',
            'linewidths': 0,
            'width': 0.1,
        }

        nx.draw_circular(UG, **options)
        plt.show()
