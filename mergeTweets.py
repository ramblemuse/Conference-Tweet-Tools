#
# *****************************************************************************
#   This script merges the tweets in two files, .json and/or .pickle created
#	by getConfTweets.py The output is either a .json or .pickle file or both.
#
#	Simplest Usage: python mergeTweets.py FILENAME1 FILENAME2
#
#   Keith Eric Grant (keg@ramblemuse.com)
#   Sat, 07 March 2015
#
# *****************************************************************************

import sys
import os
import argparse
import simplejson as json
import codecs
import pickle
import base64

myName = 'mergeTweets'

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog=myName,
        description='Parse filenames and options for merging tweet files',
        version='1.0.0')

    parser.add_argument('fn0', help='Name of first file to merge')
    parser.add_argument('fn1', help='Name of second file to merge')
    parser.add_argument('--pickle', '-p', action='store', dest='pickle', help='Pickle output file name')
    parser.add_argument('--json',   '-j', action='store', dest='json', help='JSON output file name')
    parser.add_argument('--nojson', action='store_true', default=False, help='No JSON output')
    parser.add_argument('--nopickle', action='store_true', default=False, help='No pickle output')
    parser.add_argument('--sort', '-s', action='store_true', dest='sort', default=False, help='Sort by decreasing ID')
    args = parser.parse_args(argv[1:])

    if args.pickle :
        pickleFilename = args.pickle
    else :
        pickleFilename = 'mergedTweets.pickle'
    if args.json :
        jsonFilename = args.json
    else :
        jsonFilename = 'mergedTweets.json'
		
    sortem  = args.sort	
    outputJSON   = not args.nojson
    outputPickle = not args.nopickle

    fns = (args.fn0, args.fn1)
    tweetinp = []

    for fn in fns :
        ext = os.path.splitext(fn)[1].lower()
        if ext == '.json' :
            with codecs.open(fn, 'rb', 'utf-8') as inp :
                tweets = json.load(inp)
        elif ext == '.pickle' :
            with open(fn, 'rb') as inp :
                tweets = pickle.load(inp)
        else :
            print 'Unknown extension {}'.format(ext)
            return 1
        tweetinp.extend(tweets)
        print '{}: {} tweets'.format(fn, len(tweets))

    print '{} total input tweets'.format(len(tweetinp))

    ids = set()
    tweets = []
    for tweet in tweetinp :
        id = tweet['id']
        if id not in ids :
            ids.add(id)
            tweets.append(tweet)

    print '{} merged tweets'.format(len(tweets))

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


if __name__ == "__main__":
    sys.exit(main())
