import praw
from datetime import date
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re
from envyaml import EnvYAML

secrets = EnvYAML('secrets.yaml')

client_id = secrets['reddit']['client_id']
client_secret = secrets['reddit']['client_secret']
user_agent = secrets['reddit']['user_agent']
username = secrets['reddit']['username']
password = secrets['reddit']['password']
spotify_client_id = secrets['spotify']['spotify_client_id']
spotify_client_secret = secrets['spotify']['spotify_client_secret']

reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = user_agent, username = username, password = password)
sub = reddit.subreddit("Music")

#Getting all of the top posts from today
top = sub.top(limit=50, time_filter="day")

# Creating a new spotify playlist
scope = "playlist-modify-public"
currDate = date.today().strftime("%m/%d/%y")
p_name = f"Reddit Top Music - {currDate}"

auth = SpotifyOAuth(scope=scope, client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri="https://localhost:8080")
sp = spotipy.Spotify(auth_manager=auth)
user_id = sp.me()['id']
play = sp.user_playlist_create(user_id, name=p_name, description="A playlist of the top 10 songs from r/Music")
playlist_id = play['id']

# Search for each song from reddit
track_ids = []
count = 0
for i in top:
    if(count >= 10):
        break
    track = re.match(r'.+\-.+\[.+\]', i.title)
    if(track):
        track_info = i.title.split('-', 1)
        track_title = re.sub(r'\[.*\]', '', track_info[1])
        result = sp.search(track_title + track_info[0], type='track')
        if(len(result['tracks']['items']) > 0):
            track_ids.append(result['tracks']['items'][0]['id'])
            count += 1
            print("Added " + i.title + " to the playlist")
        else:
            print("Oops, couldn't find this track on spotify: " + i.title)
    else:
        print("This post doesn't seem to be a song :(, post title: "+i.title)
# Add the songs to the playlist
sp.playlist_add_items(playlist_id, track_ids)