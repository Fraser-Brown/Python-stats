import json as json
from wordcloud import WordCloud
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import ipywidgets
from matplotlib import ticker


class Plotter:

    def structurePlot(self, tweets, retweets, replies):
        matplotlib.style.use('ggplot')

        total = tweets + retweets + replies
        labels = 'Tweets', 'Retweets', 'Replies'
        sizes = [(tweets/total) * 100, (retweets/total) * 100, (replies/total) * 100]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')

        plt.show()

    def tweetsTimeLine(self, data):
        groupbytime = data.groupby('time').count()
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
