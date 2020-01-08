import re
import time
from urllib.request import urlopen
import MySQLdb
import tweepy

host = ''
user = ''
passwd = ''
db = ''

db = MySQLdb.connect(host, user, passwd, db)

cur = db.cursor()
sql = '''RENAME TABLE tweet_list TO t1;'''
cur.execute(sql)
sql = '''CREATE TABLE tweet_list LIKE t1;'''
cur.execute(sql)
sql = '''DROP TABLE t1;'''
cur.execute(sql)

sql = '''RENAME TABLE tweeters TO t1;'''
cur.execute(sql)
sql = '''CREATE TABLE tweeters LIKE t1;'''
cur.execute(sql)
sql = '''DROP TABLE t1;'''
cur.execute(sql)

twitter_names = ['realDonaldTrump', 'TheEllenShow', 'ConanOBrien', 'BarackObama', 'jimmyfallon']

# Twitter API usernames/passwords
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''


def redirect(url):
    page = urlopen(url)
    return page.geturl()


def get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret):
    print('Getting tweets from @%s' % screen_name)

    # connect tweepy to twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    alltweets = []

    # get new tweets
    new_tweets = api.user_timeline(screen_name=screen_name, count=1, tweet_mode='extended')

    # save tweets
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    # stops after 3200?
    while len(new_tweets) > 0:
        # get tweets before oldest
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extended')

        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

        print('%s tweets downloaded' % (len(alltweets)))

    print('Tweet downloading complete')

    sql = '''INSERT INTO tweeters (username) VALUES ('%s')''' % screen_name
    cur.execute(sql)

    for tweet in alltweets:
        sqltweet = tweet.full_text
        sqltweet = re.sub(r'[^\x00-\x7f]', r'', sqltweet)
        sqltweet = re.sub(r"'", '', sqltweet)
        sqltweet = re.sub(r"&amp;", '&', sqltweet)
        sql = '''INSERT INTO tweet_list (username, tweet) VALUES ('%s', '%s')''' % (screen_name, sqltweet)
        cur.execute(sql)


if __name__ == '__main__':
    for twitter_name in twitter_names:
        get_all_tweets(twitter_name, consumer_key, consumer_secret, access_key, access_secret)

localtime = time.asctime(time.localtime(time.time()))
print(localtime)

db.commit()
cur.close()
