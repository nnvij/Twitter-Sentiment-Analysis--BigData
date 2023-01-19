from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import Stream
import json
import boto3
import time


class TweetStreamListener(Stream):
    # on success
    def on_data(self, data):
        tweet = json.loads(data)
        try:
            if 'text' in tweet.keys():
                message_lst = [str(tweet['id']),
                       str(tweet['user']['name']),
                       str(tweet['user']['screen_name']),
			     str(tweet['user']['description']),
                       tweet['text'].replace('\n',' ').replace('\r',' '),
                       str(tweet['user']['followers_count']),
                       str(tweet['user']['location']),
                       str(tweet['geo']),
                       str(tweet['created_at']),
			     str(tweet['retweet_count']),
			     str(tweet['favorite_count']),
                       '\n'
                       ]
                message = '\t'.join(message_lst)
                print(message)
                firehose_client.put_record(
                    DeliveryStreamName=delivery_stream_name,
                    Record={
                        'Data': message
                    }
                )
        except (AttributeError, Exception) as e:
            print(e)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    # create kinesis client connection
    session = boto3.Session()
    firehose_client = session.client('firehose', region_name='ca-central-1')

    # Set kinesis data stream name
    delivery_stream_name = 'Twittershutdown'

    # Set twitter credentials
    consumer_key = '**************'
    consumer_secret = '***********************************************'
    access_token = '*************************************************'
    access_token_secret = '******************************************'
  

    while True:
        try:
            print('Twitter streaming...')

            # create instance of the tweet stream listener
            stream= TweetStreamListener(consumer_key, consumer_secret,access_token, access_token_secret)

            # search twitter for the keyword
            stream.filter(track=['RIPTwitter','Twitterdown','Elon','Elon Musk','GoodByeTwitter','Twittershutdown','ElonMusk','SpaceKaren'], languages=['en'], stall_warnings=True)
        except Exception as e:
            print(e)
            print('Disconnected...')
            time.sleep(5)
            continue
