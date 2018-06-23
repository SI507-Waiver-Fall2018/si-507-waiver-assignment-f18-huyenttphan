#Huyen Phan / huyentp

# these should be the only imports you need
import tweepy
import nltk
import json
import sys

# write your code here
# usage should be python3 part1.py <username> <num_tweets>


#CACHING
CACHE = 'twittercache.json'
try:
	cache = open(CACHE, 'r')
	cache_reader = cache.read()
	TWEET_CACHE = json.loads(cache_reader)
	cache.close()
except Exception:
	TWEET_CACHE = {}

#API stuff
consumer_key = 'OYPv2sulqsdjm6cq9k4eiLKyY'
consumer_secret = 'y6ByFM0Au7G7wRlGg8iSOsYhzLZ9fcXllTZQJpCZyfJ9uJ3sij'
access_token = '841133192002248704-fxNLB4mN49MpkFuguwLA2wG0mYVr6nB'
access_token_secret = 'qlPjuFF0otQaigTLz3H3KKU5KGUm6wEqyJ5EpoR4mqtlq'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

a = sys.argv
if len(a) != 3:
	usertocheck = input('Enter a username:\n')
	tweetstocheck = input('Enter the number of tweets to be analyzed:\n')
	a = [a[0], usertocheck, tweetstocheck]
    
ident = '{1}_{2}'.format(*a)
webheader = ['http', 'https', 'RT']

def grab_tweets(user, tweets):
	userparam = {}
	if ident in TWEET_CACHE:
		print('Retrieved from cache')
		return TWEET_CACHE[ident]
	else:
		twy = api.user_timeline(user,count=tweets)
		twy_json = []
		for x in range(len(twy)):
			twy_json.append(twy[x]._json)
		TWEET_CACHE[ident] = twy_json
		dump = json.dumps(TWEET_CACHE)
		cachewrite = open(CACHE, 'w')
		cachewrite.write(dump)
		cachewrite.close()
		return TWEET_CACHE[ident]

def tweet2taggedtokens(tweet):
	dumped = json.dumps(tweet['text'])
	tokenized = [f for f in nltk.word_tokenize(dumped) if f.isalpha() and f not in webheader]
	categorized = nltk.pos_tag(tokenized)
	return categorized

#Check if person even exists in Twitter
try:
	tweetstore = grab_tweets(a[1],int(a[2]))
except Exception:
	print('User may not exist, please check in Twitter')
	sys.exit()

#Get original tweets only
original_tweet_data = {'count':0, 'favorite':0, 'retweeted':0}
tweet_collection = []

for x in tweetstore:
	for tagtuple in (tweet2taggedtokens(x)):
		tweet_collection.append(tagtuple)
	try:
		x['retweeted_status']
	except Exception:
		original_tweet_data['count'] +=1
		original_tweet_data['favorite'] += x['favorite_count']
		original_tweet_data['retweeted'] += x['retweet_count']

#Text analysis
tweet_frequency = nltk.FreqDist(tweet_collection).most_common()
nouns = sorted([(tups[0][0], tups[1]) for tups in tweet_frequency if 'NN' in tups[0][1]], key= lambda x: x[1], reverse=True)[:5]
verbs = sorted([(tups[0][0], tups[1]) for tups in tweet_frequency if 'VB' in tups[0][1]], key= lambda x: x[1], reverse=True)[:5]
adjectives = sorted([(tups[0][0], tups[1]) for tups in tweet_frequency if 'JJ' in tups[0][1]], key= lambda x: x[1], reverse=True)[:5]

def fivewordprinter(lst):
	word = ''
	for x in lst:
		word += ' {}({})'.format(*x)
	return word

#Print
print('User: {}'.format(a[1]))

if len(tweetstore) < int(a[2]):
	print('This user only has {0} tweets available.\nTWEETS ANALYZED: {0}'.format(len(tweetstore)), '\n')
else:
	print('No. of tweets analyzed: {0}'.format(int(a[2])), '\n')

print('Most frequently used verbs:\n', fivewordprinter(verbs), sep='')
print('Most frequently used nouns:\n', fivewordprinter(nouns), sep='')
print('Most frequently used adjectives:\n', fivewordprinter(adjectives), sep='')


print('Original tweets: {}'.format(original_tweet_data['count']))
print('Times Favorited (original tweets): {}'.format(original_tweet_data['favorite']))
print('Times Retweeted (original tweets): {}'.format(original_tweet_data['retweeted']))


#write to csv
csv_file = "noun_data.csv" 

csv = open(csv_file, "w") 

title_row = "Noun,Number\n"
csv.write(title_row)

for n in nouns:
	noun = n[0]
	number = str(n[1])
	row = noun + "," + number + "\n"
	csv.write(row)
