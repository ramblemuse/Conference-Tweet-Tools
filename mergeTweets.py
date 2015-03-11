#
# *****************************************************************************
#   This script merges the tweets in two files, .json and/or .pickle created
#   by getConfTweets.py The output is either a .json or .pickle file or both.
#
#   Simplest Usage: python mergeTweets.py FILENAME1 FILENAME2
#
#   options:
#       -h | --help   Print help information
#       -p | --pickle PICKLE-FILENAME
#       -j | --json   JSON-FILENAME
#       -s | --sort   Sort the tweets in descending tweet ID
#       --nojson      No JSON output (default is output)
#       --nopickle    No pickle file output (default is output)
#
#   Keith Eric Grant (keg@ramblemuse.com)
#   Tue, 10 Mar 2015
#       Removed import of base64 (not used)
#       Added version variable to globals
#       Added comments on options
#       Added option for ascending sort
#   Sat, 07 Mar 2015
#
# *****************************************************************************

import sys
import os
import argparse
import simplejson as json
import codecs
import pickle

myName = 'mergeTweets'
version = '1.0.1'

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog=myName,
        description='Parse filenames and options for merging tweet files',
        version=version)

    parser.add_argument('fn0', help='Name of first file to merge')
    parser.add_argument('fn1', help='Name of second file to merge')
    parser.add_argument('--pickle', '-p', action='store', dest='pickle', help='Pickle output file name')
    parser.add_argument('--json',   '-j', action='store', dest='json', help='JSON output file name')
    parser.add_argument('--nojson', action='store_true', default=False, help='No JSON output')
    parser.add_argument('--nopickle', action='store_true', default=False, help='No pickle output')
    parser.add_argument('--sort', '-s', action='store_true', dest='sort', default=False, help='Sort by decreasing ID')
    parser.add_argument('--ascend', '-a', action='store_true', dest='ascend', default=False, help='Use ascending sort')
    args = parser.parse_args(argv[1:])

    if args.pickle :
        pickleFilename = args.pickle
    else :
        pickleFilename = 'mergedTweets.pickle'
    if args.json :
        jsonFilename = args.json
    else :
        jsonFilename = 'mergedTweets.json'

    sortem       = args.sort
    descSort     = not args.ascend
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
        tweets.sort(key=lambda x: x['id'], reverse=descSort)

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
