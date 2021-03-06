# Conference-Tweet-Tools
Tools for gathering and analyzing tweets from conferences and chat-ups. This includes searching for tweets with a given hashtag, summarizing them as a CSV (comma separated value) file, saving them as a JSON and/or Python pickle file, and analyzing them for word-frequency or individual contributions. Note that a Twitter search using the Twitter API will only go back one week, motivating a quick and easy way to collect, concatenate, and sort such tweets as a means of curation. The tools have been tested under Python 2.7.9.

## Tools

* **getConfHashtag.py** --- Search twitter for a hashtag and save the tweets as a Python pickle file and/or a JSON file. Alternatively, load tweets from a saved pickle or JSON files and write the other filetype. Tweets can optionally be sorted by ID. Searching can be restricted by setting a lower ID corresponding, for example, to the last tweet retrieved by a prior search (which is printed out).

* **mergeTweets.py** --- Merge two saved tweet files, either pickle, JSON, or one of each. Save the merged tweets as a Python pickle file, JSON or both. Tweets can be sorted before saving.

* **filterRetweets.py** --- Read in a saved tweet file, either pickle or JSON, and filter out unedited retweets posted using the Twitter retweet capability. Save the filtered tweets as a Python pickle file, JSON, or both.  Tweets can be sorted before saving.

* **writeCSV.py** ---  Create a summary in comma separated value format (CSV) with the tweet ID, the poster's name and screen name, the timestamp, the number of retweets, the number of favorites, and the text of each tweet.

* **HTML Display**

  * **writeHTML.py** --- Reads a JSON or Python pickle file of tweets and writes the basic tweet to an HTML file with optional sorting.
  
  * **htmlWrapper.py** --- Transforms writing HTML into working with Python objects. Used by writeHTML.py
  
  * **tweet_sheet.css** --- This is the CSS stylesheet for displaying the HTML output from writeHTML.py
  
  * **imageHandler.js** --- This file contains the Javascript routines for displaying the HTML output from writeHTML.py. The routines temporary images used to speed page-loading with the real images from Twitter. they also add a pop-up image to the DOM that appears when the thumbnail image is hovered over, scaling it appropriately. for the viewport.
  
  * For examples of the HTML produced, view the tweets from these [captured conferences](http://www.ramblemuse.com/conference_tweets/). The HTML has been designed to be viewport responsive for mobile as well as desktop/laptop readability.

## Resources

* [Python Natural Language Toolkit](http://www.nltk.org/) (NLTK)
* [SixOhSix's Python wrapper](https://github.com/sixohsix/twitter) for the Twitter API
* [NetworkX](http://networkx.github.io/)
* [Mining the Social Web](http://shop.oreilly.com/product/0636920030195.do), 2nd ed.