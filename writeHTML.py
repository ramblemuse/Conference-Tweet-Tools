# -*- coding: utf-8 -*-
# ******************************************************************************
#   This routine reads in a JSON or Python pickle file containing tweets and
#   writes the tweets out as an HTML5 file. The tweets can be optionally sorted.
#   The HTML writing depends on the accompanying 'htmlWrapper' module. The HTML
#   itself depends the CSS stylesheet 'tweet_sheet.css' and the Javascript
#   file 'imageHandler.js'. The HTML produced is screen-size responsive.
#
#   Keith Eric Grant (keg@ramblemuse.com
#   04 Jul 2015
#      Switched from codecs module to io module for opens with UTF-8.
#   08 Apr 2015
#      The tweet poster's screen name now links to their Twitter page.  
#   02 Apr 2015
#
# ******************************************************************************

import sys
import os
import argparse
import simplejson as json
import io
import pickle
import re
import htmlWrapper


myName  = 'writeHTML.py'
version = '1.0.1'


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # Build the command line parser.
    parser = argparse.ArgumentParser(
        prog=myName,
        description='Display tweets as HTML',
        version=version)
    parser.add_argument('inpfile', action='store', help='Input tweet filename (.json or .pickle)')
    parser.add_argument('--html', '-m', action='store', dest='html', help='HTML output file name')
    parser.add_argument('--sort', '-s', action='store_true', dest='sort', default=False, help='Sort by decreasing ID')
    parser.add_argument('--ascend', '-a', action='store_true', dest='ascend', default=False, help='Use ascending sort')
    args = parser.parse_args(argv[1:])

    inpfile  = args.inpfile
    htmlfile = args.html if args.html else 'output.html'
    sortem   = args.sort
    descSort = not args.ascend

    # Load tweets from the input file, whether JSON or pickle.
    ext = os.path.splitext(inpfile)[1].lower()
    if ext == '.json' :
        with io.open(inpfile, 'r') as inp :
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

    # Set up a regular expression to catch retweets and avoid possible truncation
    re_text = re.compile(r'RT\s+@[_a-zA-Z0-9]+:\s')

    # Set up a regular expression to catch URLs in the text
    urlre = re.compile(r'((?:https?|ftp|file):\/\/(?:[^\s"]+))')


    doc   = htmlWrapper.document()

    # HTML Head Element
    doc_head  = doc.add_element('head')
    doc_head.add_selfclose('meta', ('charset="utf-8"',))
    doc_head.add_selfclose('meta', ('name="viewport"', 'content="width=device-width, initial-scale=1"'))
    doc_title = doc_head.add_element('title')
    doc_title.add_text('This is a title')
    doc_title.close()
    doc_head.add_selfclose('link', ('rel="stylesheet"', 'href="http://fonts.googleapis.com/css?family=Quattrocento:400,700"'))
    doc_head.add_selfclose('link', ('rel="stylesheet"', 'href="../styles/tweet_sheet.css"'))
    script = doc_head.add_element('script', ('src="../scripts/imageHandler.js"', 'defer'))
    script.close()
    doc_head.close()

    # Open HTML Body Element
    doc_body = doc.add_element('body')

    # Do the masthead
    doc_header = doc_body.add_element('div', ('id="masthead"',))
    doc_headline = doc_header.add_element('div', ('id="headline"',))
    doc_headline.add_text('Twitters')
    doc_headline.close()
    doc_tagline = doc_header.add_element('div', ('id="tagline"',))
    doc_tagline.add_text('All the Conference Tweets You Choose to Capture')
    doc_tagline.close()
    doc_header.close()

    # Create the main container, and within that the container for all tweets
    doc_cont = doc_body.add_element('div', ('id="container"',))
    doc_tweets = doc_cont.add_element('div', ('id="tweets"',))

    # Run through the individual tweets
    for tweet in tweets :
        doc_tweet = doc_tweets.add_element('div', ('class="tweet"',))

        # If the tweet has an image, add a thumbnail image element to
        # the HTML, loading a temporary image as 'src' and writing the
        # real image URL into the HTML5 data-src attribute. Javascript
        # will load the real image after page-load.

        if 'media' in tweet['entities'] :
            image = tweet['entities']['media'][0]
            imgurl = image['media_url']
            doc_tweet.add_selfclose('img', ('class="thumbnail"', \
                'src="../images/tempload_thumb.png"', \
                'data-src="{}:thumb"'.format(imgurl), \
                'alt="thumbnail"'))

        # Handle the user icon as with the image above, so that loading of
        # the real icons is delayed until after page-load.

        doc_icon = doc_tweet.add_element('div', ('class="posterimg"',))
        doc_icon.add_selfclose('img', ('src="../images/tempload_icon.png"', \
            'data-src="{}"'.format(tweet['user']['profile_image_url']), 'alt="user\'s icon"'))
        doc_icon.close()

        # Add the line with the poster's screen-name, the time-stamp, and posting software
        doc_timestamp = doc_tweet.add_element('div', ('class="timestamp"',))
        screen_name = u'<a href="https://twitter.com/{0}">@{0}</a>'.format(unicode(tweet['user']['screen_name']))
        doc_timestamp.add_text(u'{}, {}, via {}'.format(screen_name,\
           unicode(tweet['created_at']),unicode(tweet['source'])))
        doc_timestamp.close()

        # Get the text of the tweet. If it's a retweet, get the full text from
        # the RT status and prepend the RT and poster screen_name. This avoids
        # truncated RTs.

        doc_divtxt = doc_tweet.add_element('div', ('class="tweettxt"',))
        text = tweet['text']
        isrt = re_text.match(text)
        if isrt and 'retweeted_status' in tweet :
            text = isrt.group() + tweet['retweeted_status']['text']

        # Place URLs within a link, add the text, and close the tweet
        text = re.sub(urlre, r'<a href="\1">\1</a>', text)
        doc_divtxt.add_text(text)
        doc_divtxt.close()
        doc_tweet.close()

    # Close-up the document elements
    doc_tweets.close()
    doc_cont.close()
    doc_body.close()
    doc.close()

    # Write it
    with io.open(htmlfile, 'w', encoding='utf-8') as out :
        doc.write(out)


if __name__ == "__main__":
    sys.exit(main())
