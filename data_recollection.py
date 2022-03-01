from datetime import timedelta, date, datetime
import time
import os

import pandas as pd
import praw
from psaw import PushshiftAPI

# Generate start and end date for a day 
# for the range between start_date and end_date
def daterange(start_date, end_date): 
    for n in range(int((end_date - start_date).days)):
        start = start_date + timedelta(n)
        end = start_date + timedelta(n+1)
        yield (datetime(start.year, start.month, start.day), 
                datetime(end.year, end.month, end.day))

# Here you can add code for store logs in a file
def log_action(action):
    print(action)
    return

# to use PSAW
api = PushshiftAPI()

# to use PRAW
reddit = praw.Reddit(
        client_id="ADD CLIENT ID",
        client_secret="ADD CLIENT SECRET",
        user_agent="GWA data analysis (by u/USERNAME)",
)

# Here you can define the subreddits
# and the start and end date
subreddits = ['gonewildaudio']
start_date = date(2021, 1, 1)
end_date = date(2022, 1, 1)

# directory on wich to store the data
basecorpus = './datasets/'

# Iteration through subreddits to recollect data
for subreddit in subreddits:
    action = "[Subreddit] " + subreddit
    log_action(action)
    # Make a directory for the subbreddit 
    subredditdirpath = basecorpus + subreddit
    if not os.path.exists(subredditdirpath):
        os.makedirs(subredditdirpath)
    # Iteration by day
    for ts_start, ts_end in daterange(start_date, end_date):
        start_time = time.time()
        action = "\t[Date] " + ts_start.strftime("%Y-%m-%d")
        log_action(action)
        # Make a directory per day, if the directory exist, skip recollection 
        datedirpath = subredditdirpath + '/' + ts_start.strftime("%Y-%m-%d")
        if os.path.exists(datedirpath):
            continue
        else:
            os.makedirs(datedirpath)

        # CSV name
        submission_csv_path = ts_start.strftime("%Y-%m-%d") + '_' + subreddit + '_submissions.csv'
        
        # Recollected data
        submissions_dict = {
                "id" : [],
                "url" : [],
                "title": [],
                "score": [],
                "num_comments": [],
                "created_utc": [],
                "selftext": [],
        }

        # Use PSAW only to get id of submissions in time interval
        gen = api.search_submissions(
                after=int(ts_start.timestamp()),
                before=int(ts_end.timestamp()),
                filter=['id'],
                subreddit=subreddit,
                limit=None,
        )

        # Use PRAW to get actual info and traverse comment tree
        for submission_psaw in gen:
            # Use psaw here
            submission_id = submission_psaw.d_['id']
            # Use praw from now on
            submission_praw = reddit.submission(id=submission_id)

            submissions_dict["id"].append(submission_praw.id)
            submissions_dict["url"].append(submission_praw.url)
            submissions_dict["title"].append(submission_praw.title)
            submissions_dict["score"].append(submission_praw.score)
            submissions_dict["num_comments"].append(submission_praw.num_comments)
            submissions_dict["created_utc"].append(submission_praw.created_utc)
            submissions_dict["selftext"].append(submission_praw.selftext)

        # single csv file with all submissions in a day
        pd.DataFrame(submissions_dict).to_csv(datedirpath + '/' + submission_csv_path, 
                                             index=False)
        
        action = f"\t\t[Info] Found submissions: {pd.DataFrame(submissions_dict).shape[0]}"
        log_action(action)

        action = f"\t\t[Info] Elapsed time: {time.time() - start_time: .2f}s"
        log_action(action)
