import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
       
        consumer_key = 'XXXXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXX'
 
       
        try:
         
            self.auth = OAuthHandler(consumer_key, consumer_secret)
         
            self.auth.set_access_token(access_token, access_token_secret)
        
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        
        analysis = TextBlob(self.clean_tweet(tweet))
       
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_queries(self):
        '''
        Utility function to get the tweets to be queried
        from the user as comma seprated input
        '''


        query = input("Enter the hashags to query (If more than 1, then separate by comma)")
        queries = query.split(',')
        return queries

    def get_tweets(self, queries, count = 10):
        '''
        Main function to fetch tweets and parse them.
        '''
       
        tweets = []
        for query in queries:
            try:
          
                fetched_tweets = self.api.search(q = query, count = count)
 
           
                for tweet in fetched_tweets:
               
                    parsed_tweet = {}
 
               
                    parsed_tweet['text'] = tweet.text
               
                    parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                    if tweet.retweet_count > 0:
                 
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)
 
            except tweepy.TweepError as e:
                print("Error : " + str(e))
        
        return tweets
 
def main():
    api = TwitterClient()
    queries = api.get_queries()
    tweets = api.get_tweets(query = queries, count = 500)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
   
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
 
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
 
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
 
if __name__ == "__main__":

    main()
