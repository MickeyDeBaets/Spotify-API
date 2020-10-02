# Imports
import requests
import json
import urllib.parse
import base64

# Decleration of variables
searchItem = ""
clientID = ""
clientSecret = ""


# Banner to welcome user
def banner():
    print(r"""
  ___           _   _  __                _   ___ ___ 
 / __|_ __  ___| |_(_)/ _|_  _   ___    /_\ | _ \_ _|
 \__ \ '_ \/ _ \  _| |  _| || | |___|  / _ \|  _/| | 
 |___/ .__/\___/\__|_|_|  \_, |       /_/ \_\_| |___|
     |_|                  |__/                       
-----------------------------------------------------
    """)


# Banner for when no results are found
def noResults():
    print(r"""
  _  _                       _ _         __                  _ 
 | \| |___   _ _ ___ ____  _| | |_ ___  / _|___ _  _ _ _  __| |
 | .` / _ \ | '_/ -_|_-< || | |  _(_-< |  _/ _ \ || | ' \/ _` |
 |_|\_\___/ |_| \___/__/\_,_|_|\__/__/ |_| \___/\_,_|_||_\__,_|
                                                               
                                                               """)


# Function to request the auhtorization token
def tokenPOST(clientID, clientSecret):
    code = ""
    while code != 200:
        # Format and base64 encode the clientID and the client secret
        clientID = input("Insert your client ID (enter for default): ")
        clientSecret = input("Insert your client secret (enter for default): ")
        print()
        if clientID == "" or clientSecret == "":
            clientID = "................................"
            clientSecret = "................................"
        IDSecret = clientID + ":" + clientSecret
        IDSecret = IDSecret.encode('utf-8')
        IDSecret = "Basic " + str(base64.b64encode(IDSecret), "utf-8")

        # Set header and data variable, needed for token request
        headers = {'Authorization': IDSecret}
        data = {'grant_type': 'client_credentials'}

        # Send the request and return the data JSON formatted
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
        jsonToken = json.loads(response.text)
        code = response.status_code
        if code != 200:
            print("\n" + "Enter a valid ClientID and client secret!" + "\n")

    token = jsonToken["access_token"]
    return token


# Function to search an artist
def searchGET(searchItem, token):
    # Set the header with the Authorization token
    headers = {'Authorization' : "Bearer " + token}

    # Ask for artist to search
    while searchItem == "":
        searchItem = input("Type in the name of the artist: ")
    print("\n")

    # Create URL with URLencoded search item as parameter and get the results, JSON formatted
    searchItem = urllib.parse.quote(searchItem)
    url = "https://api.spotify.com/v1/search?q="
    url += searchItem + "&type=artist"
    jsonSearch = requests.get(url, headers=headers).json()
    results = jsonSearch["artists"]
    items = results["items"]
    return items


# Creating readable output from the search result
def formatOutput(items):

    # Declare lists
    lengths = []
    artists = []

    # For each artist, get their info
    for item in items:
        id = str(item["id"])
        name = str(item["name"])
        followers = str(item["followers"]["total"])
        url = str(item["external_urls"]["spotify"])
        popularity = str(item["popularity"])

        # Getting the genres out of the list
        genresList = item["genres"]
        genres = ", ".join(genresList)      

        # Add artist info as a dictionary to the artists list and get the length of the values
        artist = {"id":id, "name":name, "genres":genres, "followers":followers, "popularity":popularity, "url":url}
        lenght = [len(id), len(name), len(genres), len(followers), len(popularity), len(url)]
        artists.append(artist)
        lengths.append(lenght)
    
    # Sort the list alphabetically and add column titles and whitespace
    artists = sorted(artists, key=lambda i: i["name"])
    artists.insert(0, {"id":"ID", "name":"NAME", "genres":"GENRES", "followers":"FOLLOWERS", "popularity":"POPULARITY", "url":"URL"})
    artists.insert(1, {"id":" ", "name":" ", "genres":" ", "followers":" ", "popularity":" ", "url":" "})
    
    # Get the max length of each value
    maxLenId = max(len(artist["id"]) for artist in artists)
    maxLenName = max(len(artist["name"]) for artist in artists)
    maxLenGenres = max(len(artist["genres"]) for artist in artists)
    maxLenFollowers = max(len(artist["followers"]) for artist in artists)
    maxLenPopularity = max(len(artist["popularity"]) for artist in artists)
    maxLenUrl = max(len(artist["url"]) for artist in artists)


    # Give all the artists' values the same length as the max length of that value and print the values
    for artist in artists:
        print(str(artist["id"]) + " " * (maxLenId - len(artist["id"])), end="   ") 
        print(str(artist["name"]) + " " * (maxLenName - len(artist["name"])), end="   ") 
        print(str(artist["genres"]) + " " * (maxLenGenres - len(artist["genres"])), end="   ") 
        print(str(artist["followers"]) + " " * (maxLenFollowers - len(artist["followers"])), end="   ") 
        print(str(artist["popularity"]) + " " * (maxLenPopularity - len(artist["popularity"])), end="   ") 
        print(str(artist["url"]) + " " * (maxLenUrl - len(artist["url"])))
    print()  


# Welcome user
banner()

# Get token for user
token = tokenPOST(clientID, clientSecret)

# Check for results and print if there are any
while True:
    items = searchGET(searchItem, token)
    if len(items) == 0:
        noResults()
    else:
        formatOutput(items)
    


    