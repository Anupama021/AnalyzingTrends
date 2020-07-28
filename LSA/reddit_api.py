import requests
import json
import csv
import pandas as pd
import time


sub='stem'
before = "1594680791" #June 23rd 2020
after = "1531440000"  #January 1st 2018
subCount = 0
subStats = {}


def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/comment/?q=' + str(query) + '&size=100&after=' + str(
        after) + '&before=' + str(before) + '&subreddit=' + str(sub)
    print(url)
    r = requests.get(url)
    time.sleep(2)
    data = json.loads(r.text)
    return data['data']




def collectSubData(subm):
    subData = list()  # list to store data points
    #title = subm['title']
    body = subm['body']

    sub_id = subm['id']

    #created = datetime.datetime.fromtimestamp(subm['created_utc'])
    subData.append((sub_id, body))
    subStats[sub_id] = subData



df = pd.read_csv('STEAMKeyTerms.txt')

for index, row in df.iterrows():

    for query in row:
        data = getPushshiftData(query, after, before, sub)
        time.sleep(2)
        #while len(data) > 0:
        for submission in data:
            collectSubData(submission)
            subCount += 1

        print(len(data))




def updateSubs_file():
    upload_count = 0
    with open('reddit.csv', 'w', newline='', encoding='utf-8') as file:
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID", "Body"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count += 1

        print(str(upload_count) + " submissions have been uploaded")


updateSubs_file()


