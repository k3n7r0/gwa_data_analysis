# GWA Data Analysis
## Install dependencies
 ```
 conda env create --prefix ./env --file environment.yml
 ```
## How to use 
The script `data_recollection.py` recollect data of the posts between two dates 
for different subreddits. You need a reddit account and API credentials to use the script.
[Here](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) 
is a guide on how to create credentials for the API. 

Then you have to add them to the code.  
```python
reddit = praw.Reddit(
        client_id="ADD CLIENT ID",
        client_secret="ADD CLIENT SECRET",
        user_agent="GWA data analysis (by u/USERNAME)",
)
```

The script `concat.py` is used to concatenate all daily CSV files into one big 
CSV file. 

The script `tag_frequency.py` is used to generate a Word Cloud chart.
