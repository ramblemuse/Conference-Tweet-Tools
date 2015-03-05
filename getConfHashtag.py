#
# *****************************************************************************
#   This is a command-line Python program written as an aid for capturing
#   conference tweets for later analysis. Twitter's searches for hashtags
#   only extend back a week; there are times when something that can
#   search and capture tweets without a lot of fuss and hands-on time is
#   needed, as well as having capture as a preliminary step before analyzing
#   word-frequency and/or other aspects of the tweet record.
#
#   This program can capture the tweet record of a conference or chat as a
#   JSON file and/or a Python pickle file. It can also create a summary with
#   the tweet ID, poster's name and screen-name, time-stamp, and text of the
#   tweets as a comma separated value (CSV) file that can easily be imported
#   into Excel.
#
#   Minumum input usage: python getConfHashtag.py #hashtag
#
#   options:
#       -h | --help   Print help information
#       -p | --pickle PICKLE-FILENAME
#       -c | --csv    CSV-FILENAME
#       -j | --json   JSON-FILENAME
#       -n | --notice COUNT (default progress notice every 100 tweets)
#       -s | --sort   Sort the tweets in descending tweet ID
#       --nocsv       No CSV output (default is output)
#       --nojson      No JSON output (default is output)
#       --nopickle    No pickle file output (default is output)
#       --injson      JSON-FILENAME (input from an existing JSON file)
#       --inpickle    PICKLE-FILENAME (Input from an existing pickle file)
#
#   If output filenames aren't given, the hashtag (without the hash) is used
#   as a basename. For input from a previously created pickle file, no search
#   is done and the given hashtag is still used for an output file basename.
#
#   Keith Eric Grant (keg@ramblemuse.com)
#   Tue, 03 March 2015
#
# *****************************************************************************

import sys
import os
import argparse
import re
import time
import twitter
import simplejson as json
import codecs
import pickle
import base64


# This app's registered name with Twitter
myName = 'getConfHashtag'


def mapKey(key, enc):
    """This is a helper routine for getAppToken"""
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def getAppToken () :
    """This routine returns an application-based token from Twitter
       that works for inquiries not requiring a personal login"""

    key1 = '3sTM6ubGwujS3tw='
    key2 = 'otW6wqnYw7vg5Ng='
    key3 = 'tsaWt7ucouy5p9vj1Mno38zVubjawLi8zA=='
    key4 = 'xKee58ul2Kne3NC2pbLA36zJ1s644rC80tirzNO638Lexaev3byXu93b07ekzJnp2qo='


    # Evaluate a standard path filename for an app token for this application
    tokenFilename = os.path.normcase(os.path.expanduser('~/.twitter_appToken_{}'.format(myName)))

    # Read the needed app-token if its file exists, otherwise create and write it.
    if os.path.exists(tokenFilename) :
        token = twitter.read_bearer_token_file(tokenFilename)
        print 'Application token read from {}'.format(tokenFilename)
    else :
        # token = twitter.oauth2_dance(consumer_key, consumer_secret)
        token = twitter.oauth2_dance(mapKey(mapKey(key1,key2), key3),mapKey(mapKey(key1,key2), key4))
        twitter.write_bearer_token_file(tokenFilename, token)
        print 'Application token created and written to {}'.format(tokenFilename)

    return token


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog=myName,
        description='Parse hashtag and ouput options',
        version='1.0.0')
    parser.add_argument('hashtag', help='hashtag to search for, including #')
    parser.add_argument('--pickle', '-p', action='store', dest='pickle', help='Pickle output file name')
    parser.add_argument('--csv',    '-c', action='store', dest='csv', help='CSV output file name')
    parser.add_argument('--json',   '-j', action='store', dest='json', help='JSON output file name')
    parser.add_argument('--notice', '-n', action="store", dest='notice',type=int, default=100, help='Print processing count every n tweets')
    parser.add_argument('--nocsv',    action='store_true', default=False, help='No csv output')
    parser.add_argument('--nojson',   action='store_true', default=False, help='No JSON output')
    parser.add_argument('--nopickle', action='store_true', default=False, help='No pickle output')
    parser.add_argument('--nonotice', action='store_true', default=False, help='No processing count notices')
    parser.add_argument('--injson',   action='store', help='Load specified JSON file instead of search')
    parser.add_argument('--inpickle', action='store', help='Load specified pickle file instead of search')
    parser.add_argument('--sort', '-s', action='store_true', default='False', help='Sort by decreasing ID')
    args = parser.parse_args(argv[1:])


    hashtag = args.hashtag
    if hashtag[0] == '#' :
        basetag = hashtag[1:]
    else :
        basetag = hashtag
        hashtag = '#' + hashtag

    if args.csv :
        csvFilename = args.csv
    else :
        csvFilename = basetag + '.csv'
    if args.json :
        jsonFilename = args.json
    else :
        jsonFilename = basetag + '.json'
    if args.pickle :
        pickleFilename = args.pickle
    else :
        pickleFilename = basetag + '.pickle'

    nnotice = args.notice
    sortem  = args.sort

    outputCSV    = not args.nocsv
    outputJSON   = not args.nojson
    outputPickle = not args.nopickle

    if args.injson :

        print 'Reading JSON file {}'.format(args.injson)
        with codecs.open(args.injson, 'r') as inp :
            tweets = json.load(inp)

        total = len(tweets)
        outputJSON = False

    elif args.inpickle :

        print 'Reading pickle file {}'.format(args.inpickle)
        with open(args.inpickle, 'rb') as inp :
            tweets = pickle.load(inp)

        total = len(tweets)
        outputPickle = False

    else :

        # Authenticate with Twitter using an application token.
        api = twitter.Twitter(auth=twitter.OAuth2(bearer_token=getAppToken()))

        print 'Searching Twitter for {}'.format(hashtag)
        upper = None
        total = 0

        tweets = []
        while (True) :

            # Maximum count for a search request is 100. This loop starts with
            # the most recent matches and steps back in time by using the oldest
            # tweet in the returns as the next "upper" limit on the tweet ID. On
            # each iteration the new group of tweets extends a cumulative list.

            returns = api.search.tweets(q=hashtag, count=100, max_id=upper)
            group   = returns['statuses']

            if len(group) == 0 : break
            tweets.extend(group)
            total += len(group)
            if total % nnotice == 0 : print total

            upper = group[len(group)-1]['id']

            # Twitter rate limit for searches is 180 calls/ 15 minutes
            time.sleep(0.25)

    print '{} tweets'.format(total)

    if sortem :
        print 'Sorting tweets'
        tweets.sort(key=lambda x: x['id'], reverse=True)

    if outputPickle :
        print 'Writing pickle file {}'.format(pickleFilename)
        with open(pickleFilename, 'wb') as out :
            pickle.dump(tweets,out)

    if outputJSON :
        print 'Writing JSON file {}'.format(jsonFilename)
        with codecs.open(jsonFilename, 'w', 'utf-8') as out :
            json.dump(tweets, out, indent=4, encoding='utf-8')

    if outputCSV :
        print 'Writing CSV file {}'.format(csvFilename)

        re_crlf  = re.compile("\n|\r+")
        re_dquo  = re.compile(r'"')

        with codecs.open(csvFilename, mode='w', encoding='utf-8') as out :
            out.write('%s,%s,%s,%s,%s,%s,%s\n' % ('Tweet ID', 'Screen Name', 'Name', 'Time-Stamp', 'Retweets', 'Favorites', 'Text'))
            for tweet in tweets :
                id     = tweet['id']
                when   = tweet['created_at']

                # User is a structure within a tweet that contains
                # the poster's screen name and full name.
                user   = tweet['user']
                name   = unicode(user['name'])
                name   = re_dquo.sub(r'""', name)
                name   = '"' + name + '"'
                screen = user['screen_name']

                # The retweet and favorite counts aren't always
                # present, so they need a check and default
                if 'retweet_count' in tweet :
                    rts = tweet['retweet_count']
                else :
                    rts = 0
                if 'favorite_count' in tweet :
                    favs = tweet['favorite_count']
                else :
                    favs = 0

                # Convert the text string to a Unicode string, protect any
                # internal double quotes, remove any contained newlines,
                # and enclose in double quotes to protect any internal commas.
                text = unicode(tweet['text'])
                text = re_dquo.sub(r'""', text)
                text = re_crlf.sub(r' ', text)
                text = '"' + text + '"'

                out.write('%d,%s,%s,%s,%d,%d,%s\n' % (id, screen, name, when, rts, favs, text))


if __name__ == "__main__":
    sys.exit(main())
