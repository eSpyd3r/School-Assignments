#Author: Ethan Lim 261029610
import praw
import random
import madlibs
import time

def get_topic_comments(submission):
	"""(Submission) -> list
	Returns list of Comment objects that indicate comments and their IDs on the given url (submission)

	>>> url = 'https://www.reddit.com/r/mcgill/comments/eay2ne/mcgill_subreddit_bingo_finals_edition/'

	>>> submission = reddit.submission(url=url)

	>>> get_topic_comments(submission)
	[Comment(id='fb0vh26'), Comment(id='fb0l4dk'), Comment(id='fb15bvy'), \
	Comment(id='fb1pwq8'), Comment(id='fb26drr'), Comment(id='fj2wd6x'), \
	Comment(id='i11plzg'), Comment(id='i1fcjed'), Comment(id='i1fcjwz'), \
	Comment(id='fb1spzv'), Comment(id='fb1td2g'), Comment(id='fb1trul')]

	>>> url = 'https://www.reddit.com/r/mcgill/comments/tk6r6m/bringing_this_one_back_because_its_that_time_of/'

	>>> submission = reddit.submission(url=url)

	>>> get_topic_comments(submission)
	[Comment(id='i1ovy3f'), Comment(id='i1p1aaq'), Comment(id='i1qf83b'), Comment(id='i1p5xfd')]

	>>> url = 'https://www.reddit.com/r/NoStupidQuestions/comments/37n3w7/how_long_is_the_longest_comment_chain_on_reddit/'

	>>> submission = reddit.submission(url=url)

	>>> get_topic_comments(submission)
	[Comment(id='cro3y8b'), Comment(id='croepc9'), Comment(id='croabmw'), \
	Comment(id='croiz0w'), Comment(id='cwmo30f'), Comment(id='cro68zs'), \
	Comment(id='crodap3'), Comment(id='cron9fp'), Comment(id='crormd7'), \
	Comment(id='cro6boz'), Comment(id='cro7wwm'), Comment(id='cspjjzw'), \
	Comment(id='crosi50'), Comment(id='croecw6'), Comment(id='crov7bi'), \
	Comment(id='croz2fr'), Comment(id='crpg41o'), Comment(id='cv47qr8'), \
	Comment(id='cv4xx6e')]
	
	"""

	comment_id_list = []

	submission.comments.replace_more(limit=None) #updates original CommentForest, replacing MoreComments Objects; allows us to see children comments
	for comments in submission.comments.list(): #traverses through list of all of the comments, after replacing MoreComments objects, parsing from top-level comments downward
		comment_id_list.append(comments) #adds each comment to created list

	return comment_id_list

def filter_comments_from_authors(comment_list, author_list):
	"""(list, list) -> list
	Returns a new version of comment_list that was fitlered to only contain comments by authors in author_list

	>>> url = 'https://www.reddit.com/r/mcgill/comments/paf85s/the_only_society_we_deserve/'

	>>> submission = reddit.submission(url=url)

	>>> comments = get_topic_comments(submission)

	>>> filter_comments_from_authors(comments, ['Juan_Carl0s', 'Chicken_Nugget31'])
	[Comment(id='ha4piat'), Comment(id='ha4j1r7')]

	>>> url = 'https://www.reddit.com/r/mcgill/comments/pa6ntd/does_mcgill_have_a_taylor_swift_society/'

	>>> submission = reddit.submission(url=url)

	>>> comments = get_topic_comments(submission)

	>>> filter_comments_from_authors(comments, ['basicbitch122'])
	[Comment(id='ha4l1y0'), Comment(id='ha8kfhp'), Comment(id='ha2x3k5'), Comment(id='ha8krsq'), \
	Comment(id='ha8kgso'), Comment(id='ha8m1ll'), Comment(id='ha8m2bd'), Comment(id='ha4j5zr'), \
	Comment(id='ha8o1g9'), Comment(id='haibqxp'), Comment(id='hakivzt'), Comment(id='hadlpxs')]

	>>> url = 'https://www.reddit.com/r/mcgill/comments/tjkj68/i_accidentally_airdropped_a_dirty_pickup_line_to/'

	>>> submission = reddit.submission(url=url)

	>>> comments = get_topic_comments(submission)

	>>> filter_comments_from_authors(comments, [submission.author])
	[Comment(id='i1l7yqx')]

	"""

	filtered_comment_list = []

	for comment in comment_list:
		if comment.author in author_list: #if the author in the comment is found in author_list, comment is added to filtered list
			filtered_comment_list.append(comment)

	return filtered_comment_list


def filter_out_comments_replied_to_by_authors(comment_list, author_list):
	"""(list, list) -> list
	Returns the original comment list except for the comments that were replied to or made by an author in author_list
	
	>>> url = 'https://www.reddit.com/r/mcgill/comments/pa6ntd/does_mcgill_have_a_taylor_swift_society/'

	>>> submission = reddit.submission(url=url)

	>>> comments = get_topic_comments(submission)

	>>> filter_out_comments_replied_to_by_authors(comments, ['basicbitch122'])
	[Comment(id='ha33z5m'), Comment(id='ha2sq62'), Comment(id='ha3d39f'),\
	Comment(id='ha2s4lw'), Comment(id='ha3mrwm'), Comment(id='ha3m2kv'),\
	Comment(id='ha5okfd'), Comment(id='ha7e0ei'), Comment(id='hbpxpi1'),\
	Comment(id='ha4e526'), Comment(id='ha3837c'), Comment(id='hdo2kmm'),\
	Comment(id='ha3f5q2'), Comment(id='hdof500'), Comment(id='hdol6rn'),\
	Comment(id='hcrklp6')]

	>>> url = 'https://www.reddit.com/r/mcgill/comments/tk6r6m/bringing_this_one_back_because_its_that_time_of/'

	>>> submission = reddit.submission(url=url)

	>>> comments = get_topic_comments(submission)

	>>> filter_out_comments_replied_to_by_authors(comments, ['VardyLCFC'])
	[Comment(id='i1ovy3f'), Comment(id='i1qsdgp'), Comment(id='i1qf83b')]

	>>> url = 'https://www.reddit.com/r/mcgill/comments/tjkj68/i_accidentally_airdropped_a_dirty_pickup_line_to/'

	>>> submission = reddit.submission(url=url)

	>>> comments = get_topic_comments(submission)
	
	>>> filter_out_comments_replied_to_by_authors(comments, [submission.author])
	[Comment(id='i1l0a3x'), Comment(id='i1m5ldj'), Comment(id='i1l2rqx'), Comment(id='i1kyvhr'), \
	Comment(id='i1n5sv3'), Comment(id='i1r07ro'), Comment(id='i1lirqg'), Comment(id='i1o5ugr'), \
	Comment(id='i1lpwsh'), Comment(id='i1lpu59')]

	"""

	comments_to_remove_list = []
	comment_list_iterate = comment_list[0:] #as we are modifying the original list, need to make a copy of the originial that remains the same when iterating through
	
	for comment in comment_list_iterate: 
		if comment.author in author_list:
			comment_list.remove(comment)
			comments_to_remove_list.append(comment) #to keep track of parent comments, in case the comment is a reply, we add to separe list to check parent type (sub, or comment)
	
	for comment_to_remove in comments_to_remove_list:
		parent = comment_to_remove.parent() #gathers information on parent comment (or submission, of top level)

		if type(parent) == praw.models.reddit.comment.Comment and parent in comment_list: #ensures the parent is a comment itself and that it hasn't already been removed
			comment_list.remove(parent)

	return comment_list

def get_authors_from_topic(submission):
	"""(Submission) -> dict
	Returns dictionary from submission that contains keys that are the authors on the submission whose values represent the number of comments that author has made

	>>> url = 'https://www.reddit.com/r/mcgill/comments/pa6ntd/does_mcgill_have_a_taylor_swift_society/'

	>>> submission = reddit.submission(url=url)

	>>> num_comments_per_author = get_authors_from_topic(submission)

	>>> len(num_comments_per_author)
	31

	>>> num_comments_per_author['basicbitch122']
	12
	
	>>> url = 'https://www.reddit.com/r/mcgill/comments/tmx60p/spring_2022_convocation/'

	>>> submission = reddit.submission(url=url)

	>>> num_comments_per_author = get_authors_from_topic(submission)

	>>> len(num_comments_per_author)
	1

	>>> num_comments_per_author['Gstormborn']
	1

	>>> url = 'https://www.reddit.com/r/mcgill/comments/tkiykr/laptop_recommendations/'

	>>> submission = reddit.submission(url=url)

	>>> len(num_comments_per_author)
	21

	>>> num_comments_per_author[submission.author.name]
	2
	"""
	
	comment_list = get_topic_comments(submission)
	commentors = []
	for comment in comment_list:
		if comment.author not in commentors and comment.author != None: #in case of duplicates and deleted users
			commentors.append(comment.author.name) 

	commentor_value_pairs = []
	for commentor in commentors:
		commentor_comment_list = filter_comments_from_authors(comment_list, [commentor]) #filters list of comments by author
		commentor_value_pairs.append((commentor, len(commentor_comment_list))) #creates tuple, representing the author and the length of their comment list (number of comments they've made)

	return dict(commentor_value_pairs)

def select_random_submission_url(reddit, t_url, subreddit, limit):
	"""(Reddit, str, str, int) -> Submission
	Returns submission object depending on dice roll
	"""

	dice_roll = random.randint(1, 6) #generates random number

	if dice_roll == 1 or dice_roll == 2:
		submission = reddit.submission(url=t_url)
		submission.comments.replace_more(limit=limit) #loads comments

		return submission

	else:
		subreddit = reddit.subreddit(subreddit).top('all')

		submission_list = [] #list of top submissions
		for submission in subreddit:
			submission_list.append(submission)

		return random.choice(submission_list)


def post_reply(submission, username):
	"""(Submission, str) -> none
	Posts reply to given submission, depending on if username has already made a reply to submission

	"""
	authors = get_authors_from_topic(submission) #all authors on a given submission
	my_comment = madlibs.generate_comment() #generates comment to post

	if username not in authors:
		submission.reply(my_comment)
	else:
		reply_to = random.choice(get_topic_comments(submission))
		reply_to.reply(my_comment)



def bot_daemon(reddit, s_url, limit, subreddit, username):
	"""(Reddit, str, int, str, str) -> none
	Automatically posts replies, starting at submission s_url under subreddit while indentifying as username
	"""
	while True:
		submission = select_random_submission_url(reddit, s_url, subreddit, limit) #collects submission to post on
		post_reply(submission, username)
		time.sleep(60) #waits 60 seconds before next iteration


if __name__ == "__main__":
	reddit = praw.Reddit('bot', config_interpolation="basic")
