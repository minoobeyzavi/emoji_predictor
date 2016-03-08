from pyspark import SparkContext
import json
import re
import nltk


# start spark instance
sc = SparkContext()


# REGEX for finding emoji

REGEX = u"[\U00002712\U00002714\U00002716\U0000271d\U00002721\U00002728\U00002733\U00002734\U00002744\U00002747\U0000274c\U0000274e\U00002753-\U00002755\U00002757\U00002763\U00002764\U00002795-\U00002797\U000027a1\U000027b0\U000027bf\U00002934\U00002935\U00002b05-\U00002b07\U00002b1b\U00002b1c\U00002b50\U00002b55\U00003030\U0000303d\U0001f004\U0001f0cf\U0001f170\U0001f171\U0001f17e\U0001f17f\U0001f18e\U0001f191-\U0001f19a\U0001f201\U0001f202\U0001f21a\U0001f22f\U0001f232-\U0001f23a\U0001f250\U0001f251\U0001f300-\U0001f321\U0001f324-\U0001f393\U0001f396\U0001f397\U0001f399-\U0001f39b\U0001f39e-\U0001f3f0\U0001f3f3-\U0001f3f5\U0001f3f7-\U0001f4fd\U0001f4ff-\U0001f53d\U0001f549-\U0001f54e\U0001f550-\U0001f567\U0001f56f\U0001f570\U0001f573-\U0001f579\U0001f587\U0001f58a-\U0001f58d\U0001f590\U0001f595\U0001f596\U0001f5a5\U0001f5a8\U0001f5b1\U0001f5b2\U0001f5bc\U0001f5c2-\U0001f5c4\U0001f5d1-\U0001f5d3\U0001f5dc-\U0001f5de\U0001f5e1\U0001f5e3\U0001f5ef\U0001f5f3\U0001f5fa-\U0001f64f\U0001f680-\U0001f6c5\U0001f6cb-\U0001f6d0\U0001f6e0-\U0001f6e5\U0001f6e9\U0001f6eb\U0001f6ec\U0001f6f0\U0001f6f3\U0001f910-\U0001f918\U0001f980-\U0001f984\U0001f9c0\U00003297\U00003299\U000000a9\U000000ae\U0000203c\U00002049\U00002122\U00002139\U00002194-\U00002199\U000021a9\U000021aa\U0000231a\U0000231b\U00002328\U00002388\U000023cf\U000023e9-\U000023f3\U000023f8-\U000023fa\U000024c2\U000025aa\U000025ab\U000025b6\U000025c0\U000025fb-\U000025fe\U00002600-\U00002604\U0000260e\U00002611\U00002614\U00002615\U00002618\U0000261d\U00002620\U00002622\U00002623\U00002626\U0000262a\U0000262e\U0000262f\U00002638-\U0000263a\U00002648-\U00002653\U00002660\U00002663\U00002665\U00002666\U00002668\U0000267b\U0000267f\U00002692-\U00002694\U00002696\U00002697\U00002699\U0000269b\U0000269c\U000026a0\U000026a1\U000026aa\U000026ab\U000026b0\U000026b1\U000026bd\U000026be\U000026c4\U000026c5\U000026c8\U000026ce\U000026cf\U000026d1\U000026d3\U000026d4\U000026e9\U000026ea\U000026f0-\U000026f5\U000026f7-\U000026fa\U000026fd\U00002702\U00002705\U00002708-\U0000270d\U0000270f]|[#]\U000020e3|[*]\U000020e3|[0]\U000020e3|[1]\U000020e3|[2]\U000020e3|[3]\U000020e3|[4]\U000020e3|[5]\U000020e3|[6]\U000020e3|[7]\U000020e3|[8]\U000020e3|[9]\U000020e3|\U0001f1e6[\U0001f1e8-\U0001f1ec\U0001f1ee\U0001f1f1\U0001f1f2\U0001f1f4\U0001f1f6-\U0001f1fa\U0001f1fc\U0001f1fd\U0001f1ff]|\U0001f1e7[\U0001f1e6\U0001f1e7\U0001f1e9-\U0001f1ef\U0001f1f1-\U0001f1f4\U0001f1f6-\U0001f1f9\U0001f1fb\U0001f1fc\U0001f1fe\U0001f1ff]|\U0001f1e8[\U0001f1e6\U0001f1e8\U0001f1e9\U0001f1eb-\U0001f1ee\U0001f1f0-\U0001f1f5\U0001f1f7\U0001f1fa-\U0001f1ff]|\U0001f1e9[\U0001f1ea\U0001f1ec\U0001f1ef\U0001f1f0\U0001f1f2\U0001f1f4\U0001f1ff]|\U0001f1ea[\U0001f1e6\U0001f1e8\U0001f1ea\U0001f1ec\U0001f1ed\U0001f1f7-\U0001f1fa]|\U0001f1eb[\U0001f1ee-\U0001f1f0\U0001f1f2\U0001f1f4\U0001f1f7]|\U0001f1ec[\U0001f1e6\U0001f1e7\U0001f1e9-\U0001f1ee\U0001f1f1-\U0001f1f3\U0001f1f5-\U0001f1fa\U0001f1fc\U0001f1fe]|\U0001f1ed[\U0001f1f0\U0001f1f2\U0001f1f3\U0001f1f7\U0001f1f9\U0001f1fa]|\U0001f1ee[\U0001f1e8-\U0001f1ea\U0001f1f1-\U0001f1f4\U0001f1f6-\U0001f1f9]|\U0001f1ef[\U0001f1ea\U0001f1f2\U0001f1f4\U0001f1f5]|\U0001f1f0[\U0001f1ea\U0001f1ec-\U0001f1ee\U0001f1f2\U0001f1f3\U0001f1f5\U0001f1f7\U0001f1fc\U0001f1fe\U0001f1ff]|\U0001f1f1[\U0001f1e6-\U0001f1e8\U0001f1ee\U0001f1f0\U0001f1f7-\U0001f1fb\U0001f1fe]|\U0001f1f2[\U0001f1e6\U0001f1e8-\U0001f1ed\U0001f1f0-\U0001f1ff]|\U0001f1f3[\U0001f1e6\U0001f1e8\U0001f1ea-\U0001f1ec\U0001f1ee\U0001f1f1\U0001f1f4\U0001f1f5\U0001f1f7\U0001f1fa\U0001f1ff]|\U0001f1f4\U0001f1f2|\U0001f1f5[\U0001f1e6\U0001f1ea-\U0001f1ed\U0001f1f0-\U0001f1f3\U0001f1f7-\U0001f1f9\U0001f1fc\U0001f1fe]|\U0001f1f6\U0001f1e6|\U0001f1f7[\U0001f1ea\U0001f1f4\U0001f1f8\U0001f1fa\U0001f1fc]|\U0001f1f8[\U0001f1e6-\U0001f1ea\U0001f1ec-\U0001f1f4\U0001f1f7-\U0001f1f9\U0001f1fb\U0001f1fd-\U0001f1ff]|\U0001f1f9[\U0001f1e6\U0001f1e8\U0001f1e9\U0001f1eb-\U0001f1ed\U0001f1ef-\U0001f1f4\U0001f1f7\U0001f1f9\U0001f1fb\U0001f1fc\U0001f1ff]|\U0001f1fa[\U0001f1e6\U0001f1ec\U0001f1f2\U0001f1f8\U0001f1fe\U0001f1ff]|\U0001f1fb[\U0001f1e6\U0001f1e8\U0001f1ea\U0001f1ec\U0001f1ee\U0001f1f3\U0001f1fa]|\U0001f1fc[\U0001f1eb\U0001f1f8]|\U0001f1fd\U0001f1f0|\U0001f1fe[\U0001f1ea\U0001f1f9]|\U0001f1ff[\U0001f1e6\U0001f1f2\U0001f1fc]|[0-9*#]\ufe0f\u20e3"


def tweet_process(tweet):
    KEY = 'text'
    try:
        tw = json.loads(tweet.strip())
        if KEY not in tw or tw['lang']!= 'en':
            return None
        return tw

    except Exception as e:
        return None


def emoji_preprocess(tweet):
    # add space before and after space
    for emoji in re.findall(REGEX, tweet):
        tweet = tweet.replace(emoji, ' ' + emoji + ' ')

    # tokenize and remove rt and @ and https://

    tweet_token = ['<s>'] + [ wd for wd in tweet.strip('rt').split() if not wd.startswith('@') and not wd.startswith('http') and not wd.startswith('#') ] + ['</s>']

    return tweet_token


def bigrams(tweet):
    # generate bigrams from tweets
    return list(nltk.bigrams(tweet))

def trigrams(tweet):
    # generate trigrams from tweets
    return [((w1, w2), w3) for w1, w2, w3 in nltk.trigrams(tweet)]

def quadgrams(tweet):
    #generate n grams
    return [((w1, w2, w3), w4) for w1, w2, w3, w4 in nltk.ngrams(tweet, 4)]




if __name__ == '__main__':
    tweets =  sc.textFile('data/twitter_dump_small.txt')\
    .filter(lambda tw: len(tw)>1)\
    .filter(lambda tw: 'created_at' in tw)\
    .map(tweet_process)\
    .filter(lambda tw: tw != None)\
    .map(lambda tw: tw['text'].lower() )\

    tweets_tokens = tweets.map(emoji_preprocess).collect()  # I should split the word into token and bigram and count with reduce by key

    bigram_count = tweets.map(emoji_preprocess).flatMap(bigrams).map(lambda bg: (bg, 1)).reduceByKey(lambda cnt1, cnt2: cnt1+cnt2).collect()
    trigram_count = tweets.map(emoji_preprocess).flatMap(trigrams).map(lambda bg: (bg, 1)).reduceByKey(lambda cnt1, cnt2: cnt1+cnt2).collect()



# I have not preprocess (stem, lematize)
