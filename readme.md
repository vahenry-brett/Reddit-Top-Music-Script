# Reddit r/Music top songs script

This script scrapes the top posts off of r/Music from the past day, and creates a spotify playlist with the top 10 songs

## Dependencies
Python 3.9.1
Install some of the other dependencies with:
~~~
pip install spotipy
pip install praw
pip install envyaml
~~~

## Env Vars
You need to set a few environment variables to use the reddit and spotify apis, check secrets.yaml for a full list. In order to use this script you have to register with both reddit and spotify, which you can do here: https://www.reddit.com/prefs/apps and https://developer.spotify.com/dashboard/applications

Once you've registered on both sites you can fill in the env vars with the client_ids, client_secrets (for both spotify and reddit) and then for reddit only also add your username, password, and user_agent (the name of the script that you registered).
