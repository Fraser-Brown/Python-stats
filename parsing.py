import pandas as pd
import numpy as np

class CensusReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = pd.read_csv(fileName)

        self.data["valid"] = True
        self.validateFile()

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
        for i, v in texts.iteritems():
            if type(v) is not str:
                continue
            if(v[0:4] == "RT @"):
                counts += 1
        return counts

    def replyCount(self):
        texts = self.data.loc[:, "in_reply_to_screen_name"]
        counts = 0
        for v in texts:
            if type(v) is str:
                counts += 1
        return counts

    def tweetCount(self):
        result = len(self.data) - self.retweetCount() - self.replyCount()
        return result

    def numOfUsers(self):
        newData = self.data.drop_duplicates(subset=['from_user_id_str'])
        print(len(newData))

    def mostPopHashtags(self):
        print(self.data.groupby('entities_str').count().sort_values(by=['id_str'], ascending=False).head(1))
