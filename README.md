# STAS-Scriptie

This is a bot for [/r/shittheadminssay](https://reddit.com/r/shittheadminssay), a
subreddit dedicated to showing the most interesting comments and posts that the admins
make.

## What does Scriptie do?

Roughly every hour(?):

- Downloads all of the admins comments from the last month.  This is done using the
  friends system and the Reddit API.
- Posts any new, unseen comments to [/r/stas-posts](https://reddit.com/r/stas-posts).
- Inserts any new, unseen comments into a database, and updates the comment scores of all
  comments currently in that database.
- Removes any posts older than one month(?) from the database.


## TODO:

- Scrape the list of admins and add them all as friends.
