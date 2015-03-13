
# *****************************************************************************
#
#   Input tweets saved as either a JSON or a Python Pickle file and write the
#   Twitter ID, poster's name and screen_name, timestamp, number of tweets,
#   number of favorites, and the tweet text as a comma separated value file 
#   (CSV). Tested with Python 2.7.9
#
#   Simplest usage: python writeCSV.py INPUT-FILENAME
#
#   options:
#       -h | --help   Print help information
#       -c | --csv    CSV-FILENAME
#       -s | --sort   Sort the tweets in descending tweet ID
#       -a | --ascend Use ascending order if sort  is selected
#
#   Keith Eric Grant (keg@ramblemuse.com)
#   13 Mar 2015
#
# *****************************************************************************

import sys
import os
import argparse
import simplejson as json
import codecs
import pickle
import re


myName  = 'writeCSV.py'
version = '1.0.0'


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog=myName,
        description='Write a CSV summary of collected tweets',
        version=version)
    parser.add_argument('inpfile', action='store', help='Input tweet filename (.json or .pickle)')
    parser.add_argument('--csv', '-c', action='store', dest='csv', help='CSV output file name')
    parser.add_argument('--sort', '-s', action='store_true', dest='sort', default=False, help='Sort by decreasing ID')
    parser.add_argument('--ascend', '-a', action='store_true', dest='ascend', default=False, help='Use ascending sort')
    args = parser.parse_args(argv[1:])

    inpfile  = args.inpfile
    sortem   = args.sort
    descSort = not args.ascend

    csvFilename = args.csv if args.csv else 'tweets.csv'

    # Load tweets from the input file, whether JSON or pickle.
    ext = os.path.splitext(inpfile)[1].lower()
    if ext == '.json' :
        with codecs.open(inpfile, 'rb', 'utf-8') as inp :
            tweets = json.load(inp)
    elif ext == '.pickle' :
        with open(inpfile, 'rb') as inp :
            tweets = pickle.load(inp)
    else :
        print 'Unknown extension {}'.format(ext)
        return 1

    print '{}: {} tweets'.format(inpfile, len(tweets))

    if sortem :
        print 'Sorting tweets'
        tweets.sort(key=lambda x: x['id'], reverse=descSort)


    print 'Writing CSV file {}'.format(csvFilename)

    re_crlf  = re.compile("\n|\r+")
    re_dquo  = re.compile(r'"')

    with codecs.open(csvFilename, mode='w', encoding='utf-8') as out :
        out.write('%s,%s,%s,%s,%s,%s,%s\n' % ('Tweet ID', 'Screen Name', 'Name',
           'Time-Stamp', 'Retweets', 'Favorites', 'Text'))
        for tweet in tweets :
            id     = tweet['id_str']
            when   = tweet['created_at']

            # User is a structure within a tweet that contains the poster's
            # screen name and full name. Convert the name to a Unicode string,
            # protect any internal double quotes, and enclose in double quotes
            # to protect any internal commas.

            user   = tweet['user']
            name   = unicode(user['name'])
            name   = re_dquo.sub(r'""', name)
            name   = '"' + name + '"'
            screen = user['screen_name']

            # The retweet and favorite counts aren't always present, so
            # they need a check and a default.
            rts  = tweet['retweet_count']  if 'retweet_count'  in tweet else 0
            favs = tweet['favorite_count'] if 'favorite_count' in tweet else 0

            # Convert the text string to a Unicode string, protect any
            # internal double quotes, remove any contained newlines,
            # and enclose in double quotes to protect any internal commas.

            text = unicode(tweet['text'])
            text = re_dquo.sub(r'""', text)
            text = re_crlf.sub(r' ', text)
            text = '"' + text + '"'

            out.write('%s,%s,%s,%s,%d,%d,%s\n' % (id, screen, name, when, rts, favs, text))

if __name__ == "__main__":
    sys.exit(main())
