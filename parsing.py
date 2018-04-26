import pandas as pd
import numpy as np
from operator import itemgetter
import json
from collections import Counter

class CensusReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = pd.read_csv(fileName)

        self.data["valid"] = True
        self.validateFile()

    def removeDuplicates(self, seq):
        # Not order preserving
        keys = {}
        for e in seq:
            keys[e] = 1
        return keys.keys()

    def validateFile(self):
        #check duplication
        self.data["valid"] = self.data["valid"] & ~(self.data.duplicated("id_str"))

        invalidData = self.data.query("valid == False")
        self.data = self.data.query("valid == True")

        # Drops the 'valid' column since it is no longer needed.
        self.data.drop('valid', axis=1, inplace=True)

        invalidRows = len(invalidData)

        if (invalidRows > 0):
            if invalidRows == 1:
                print("File contains 1 invalid row!")
            else:
                print("File contains "+str(invalidRows)+ " invalid rows!")

            #make a new file
            if self.fileName[-4:] == ".csv":
                print("Refining the data given and storing it a new file...")
                newFileName = self.fileName[:-4] + "_refined.csv"
                self.data.to_csv(newFileName)
                print("Refined data can be found in \'" + newFileName + "\'.")

    def retweetCount(self):
        texts = self.data.loc[:,"text"]
        counts = 0
        for v in texts.iteritems():
            if type(v) is not str:
                continue
            if(v[0:4] == "RT @"):
                counts += 1
        return counts

    def replyCount(self):
        replytweets = self.data.loc[:, "in_reply_to_screen_name"]
        counts = 0
        for v in replytweets:
            if type(v) is str:
                counts += 1
        return counts

    def tweetCount(self):
        result = len(self.data.loc[:, 'entities_str']) - self.replyCount() - self.retweetCount()
        return result

    def userCount(self):
        tweetsWithUniqueUsers = self.data.drop_duplicates(subset=['from_user_id_str'])
        return len(tweetsWithUniqueUsers)
    
    def getHashTags(self):
        #     hashtags = self.data.groupby('entities_str').count().sort_values(by=['id_str'], ascending=False).head(number)
        data = self.data
        hashtags = []
        jsonItems = data.loc[:, 'entities_str'] # lst of JSON hashtag items
        # each JSON hashtag item has syntax: {""hashtags"":[{""text"":""67P"",""indices"":[58,62]},{""text"":""CometWatch"",""indices"":[127,138]},{""text"":""CometLanding"",""indices"":[139,140]}],""symbols"":[],""user_mentions"":[{""screen_name"":""ESA_Rosetta"",""name"":""ESA Rosetta Mission"",""id"":253536357,""id_str"":""253536357"",""indices"":[3,15]}],""urls"":[{""url"":""http://t.co/Z2A14Jorv6"",""expanded_url"":""http://youtu.be/4a3eY5siRRk"",""display_url"":""youtu.be/4a3eY5siRRk"",""indices"":[104,126]}]}".
        for JSONString in jsonItems:
            if not type(JSONString) is str: continue
            parsedJSON = json.loads(JSONString)
            JSONHashTagsElement = parsedJSON['hashtags']
            for JSONHashTag in JSONHashTagsElement:
                hashtags.append(JSONHashTag['text'])
        return hashtags
    
    def getHTagsAndCounts(self):
        hashtags = sorted(self.getHashTags(), reverse=False)
        hashtagsNoDuplicates = self.removeDuplicates(hashtags)
        hTagsAndCounts = []
        counter = Counter(hashtags)
        for ht in hashtagsNoDuplicates:
            count = counter[ht] # hashtags.count(ht)
            hTagsAndCounts.append([ht, count])
        return hTagsAndCounts

    def mostPopHashtags(self, number):
        sortedHTagsAndCounts = sorted(self.getHTagsAndCounts(), key = itemgetter(1), reverse=True)
        returnString = ""
        for x in range(0,number):
            returnString += str(x + 1) + ". #" + sortedHTagsAndCounts[x][0] + " : " + str(sortedHTagsAndCounts[x][1]) + " tweets (of any type)\n"
        return returnString