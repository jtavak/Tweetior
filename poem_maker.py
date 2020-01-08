import random
import string
import pronouncing


# find if the inputted word rhymes with any of the dictionary keys
def find_rhyming_tweets(rhymeswith, tweetdict):
    rhymes = pronouncing.rhymes(rhymeswith)
    for rhyme in rhymes:
        try:
            return tweetdict[rhyme]
        except Exception:
            pass


def create_poem(min_words_per_line, max_words_per_line, line_count, screen_name, cur):
    sql = """SELECT tweet FROM tweet_list WHERE username = '%s'""" % (screen_name)
    cur.execute(sql)
    tweets = list(cur)
    raw_tweets = [j for sub in tweets for j in sub]

    sentences = []  # list of all sentences to use
    tweetdict = {}  # dictionary {last letter: full sentence}

    # split each tweet into sentences
    for tweet in raw_tweets:
        tweet = tweet.split('.')
        for sentence in tweet:
            # if the sentence is too short or long do not use
            if sentence is not '' and len(sentence.split()) < max_words_per_line + 1 and len(
                    sentence.split()) > min_words_per_line - 1:
                sentences.append(sentence)

    # for each sentence set the dictionary key as the last word
    for sentence in sentences:
        dictkey = sentence.split()[-1]
        exclude = set(string.punctuation)
        dictkey = ''.join(ch for ch in dictkey if ch not in exclude)
        tweetdict[dictkey] = sentence

    keys = list(tweetdict.keys())
    random.seed()
    random.shuffle(keys)

    poem = []
    poem.extend(['A poem by @%s' % screen_name])

    loops = 0
    while loops < line_count:
        if find_rhyming_tweets(keys[1], tweetdict):
            poem.extend([tweetdict[keys[1]], find_rhyming_tweets(keys[1], tweetdict)])
            loops += 2
        random.shuffle(keys)

    return poem


def get_twitter_poem(long_poem):
    short_poem = []
    for i in range(len(long_poem)):
        if len(''.join(short_poem)) + len(long_poem[i]) < 240:
            short_poem.append(long_poem[i])

    return short_poem
