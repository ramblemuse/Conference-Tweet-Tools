
# *****************************************************************************
#   This routine filters out unedited retweets created using the Twitter
#   retweet capability. The input is a JSON or Python pickle file of
#   tweets captured by getConfHashtag.py The output is a filtered JSON or
#   pickle file or both (default)
#
#   Simplest usage: python filterRetweets.py INPUT-FILENAME
#
#   options:
#       -h | --help   Print help information
#       -p | --pickle PICKLE-FILENAME
#       -j | --json   JSON-FILENAME
#       -s | --sort   Sort the tweets in descending tweet ID
#       -a | --ascend Use ascending order if sort  is selected
#       --nojson      No JSON output (default is output)
#       --nopickle    No pickle file output (default is output)
#
#   Keith Eric Grant (keg@ramblemuse.com)
#   10 Mar 2015
#
# *****************************************************************************

import sys
import os
import argparse
import simplejson as json
import codecs
import pickle


myName  = 'filtertweets'
version = '1.0.0'


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(
        prog=myName,
        description='Filter out unedited retweets',
        version=version)
    parser.add_argument('inpfile', action='store', help='Input tweet filename (.json or .pickle)')
    parser.add_argument('--pickle', '-p', action='store', dest='pickle', help='Pickle output file name')
    parser.add_argument('--json',   '-j', action='store', dest='json', help='JSON output file name')
    parser.add_argument('--nojson',   action='store_true', default=False, help='No JSON output')
    parser.add_argument('--nopickle', action='store_true', default=False, help='No pickle output')
    parser.add_argument('--sort', '-s', action='store_true', dest='sort', default=False, help='Sort by decreasing ID')
    parser.add_argument('--ascend', '-a', action='store_true', dest='ascend', default=False, help='Use ascending sort')
    args = parser.parse_args(argv[1:])

    inpfile = args.inpfile
    sortem  = args.sort

    pickleFilename = args.pickle if args.pickle else 'noretweets.pickle'
    jsonFilename   = args.json if args.json else 'noretweets.json'
    outputJSON     = not args.nojson
    outputPickle   = not args.nopickle
    descSort       = not args.ascend

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

    # If this is a Twitter retweet, there's a status field
    tweets = [x for x in tweets if not 'retweeted_status' in x]

    print '{} tweets without retweets'.format(len(tweets))

    if sortem :
        print 'Sorting tweets'
        tweets.sort(key=lambda x: x['id'], reverse=descSort)

    if outputPickle :
        print 'Writing pickle file {}'.format(pickleFilename)
        with open(pickleFilename, 'wb') as out :
            pickle.dump(tweets,out)

    if outputJSON :
        print 'Writing JSON file {}'.format(jsonFilename)
        with codecs.open(jsonFilename, 'wb', 'utf-8') as out :
            json.dump(tweets, out, indent=4, encoding='utf-8')

if __name__ == "__main__":
    sys.exit(main())
