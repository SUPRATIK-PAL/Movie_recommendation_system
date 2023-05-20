import requests as r
import urllib

def grab_movie_details(movie_name):
    url = "http://www.omdbapi.com/?apikey=e72419cf&t="
    url += urllib.parse.quote(movie_name)
    data = r.get(url)

    return data.json()
