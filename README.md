# Conference-Tweet-Tools
Tools for gathering and analyzing tweets from conferences and chat-ups. This includes searching for tweets with a given hashtag, summarizing them as a CSV (comma separated value) file, saving them as a JSON and/or Python pickle file, and analyzing them for word-frequency or individual contributions. Note that a Twitter search using the Twitter API will only go back one week, motivating a quick and easy way to collect, concatenate, and sort such tweets as a means of curation.

## Tools

* getConfHashtag.py --- Search twitter for a hashtag and save the tweets as a Python pickle file and/or a JSON file. Create a summary with the text of the tweets as a CSV file. Alternatively, load tweets from a saved pickle or JSON files and write the other filetypes. Tweets can optionally be sorted by ID.

* mergeTweets.py --- Merge two saved tweet files, either pickle, JSON, or one of each. Save the merged tweets as a Python pickle file, JSON or both. Tweets can be sorted before saving.

* filterRetweets.py --- Read in a saved tweet file, either pickle or JSON, and filter out unedited retweets posted using the Twitter retweet capability. Save the filtered tweets as a Python pickle file, JSON, or both.  Tweets can be sorted before saving.
