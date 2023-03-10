import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# *---------------------------------- CONSTANTS ----------------------------------* #
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URL = "http://example.com"
SCOPE = "playlist-modify-private"

date = input("What year you would like to travel to in YYYY-MM-DD: ")

# Making soup
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
webpage = response.content
soup = BeautifulSoup(webpage, "html.parser")

# Create a list of songs
song_1 = soup.find(name="a", class_="c-title__link lrv-a-unstyle-link")
h3_tags = soup.find_all(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                          "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                          "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                          "u-max-width-230@tablet-only")

title_1 = song_1.get_text().strip()
songs = [tag.get_text().strip() for tag in h3_tags]
songs.insert(0, title_1)

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              redirect_uri=REDIRECT_URL,
                              scope=SCOPE,
                              cache_path="token.txt",
                              show_dialog=True
                              )
                    )
user_id = sp.current_user()["id"]

# create list of song uri's
year = date.split('-')[0]
print(year)
song_uris = []
for song in songs:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{year} - Billboard's top 100", public=False, collaborative=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)

