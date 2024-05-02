import sys,  re

import praw
class TweetSearch:

    def search(keys):
        tweetset = []

        try:
            

            client_id = 'msVOcvbKWhwpdfqFJLrlZw'
            client_secret = 'rK_rRaeS3DOj2Fp_lP2ecFW_b4vHNg'
            user_agent = 'praw_scraper_1'
        
            reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)# input for term to be searched and how many tweets to search
            
            
        
            searchTerm = keys
            max_posts = 10
            posts = reddit.subreddit('all').search(searchTerm, limit=max_posts)
            for post in posts:
                tweetset.append(str(post.title))

            
        except Exception as e:
            print(e)
        print("SSSSSSSSSSS")
        return tweetset


if __name__ == '__main__':
    TweetSearch.search('Telangana')