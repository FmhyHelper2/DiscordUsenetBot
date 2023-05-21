import requests

imdbId = "tt3581920"
url = f"https://api.tvmaze.com/lookup/shows?imdb={imdbId}"
res = requests.get(url)
if res:
    print(res.json()["id"])
else:
    print(res)
