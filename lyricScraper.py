import requests
import json
import time
import os

API_URL = "https://api.lyrics.ovh/v1/{artist}/{title}"

# List of pop songs to fetch lyrics for (artist, title)
POP_SONGS = [
    ("Teddy Swims", "'Lose Control'"),
    ("Shaboozey", "'A Bar Song (Tipsy)'"),
    ("Benson Boone", "'Beautiful Things'"),
    ("Post Malone featuring Morgan Wallen", "'I Had Some Help'"),
    ("Jack Harlow", "'Lovin on Me'"),
    ("Kendrick Lamar", "'Not Like Us'"),
    ("Sabrina Carpenter", "'Espresso'"),
    ("Tommy Richman", "'Million Dollar Baby'"),
    ("Zach Bryan featuring Kacey Musgraves", "'I Remember Everything'"),
    ("Hozier", "'Too Sweet'"),
    ("Noah Kahan", "'Stick Season'"),
    ("Taylor Swift", "'Cruel Summer'"),
    ("Tate McRae", "'Greedy'"),
    ("Future, Metro Boomin and Kendrick Lamar", "'Like That'"),
    ("Billie Eilish", "'Birds of a Feather'"),
    ("Sabrina Carpenter", "'Please Please Please'"),
    ("Doja Cat", "'Agora Hills'"),
    ("Chappell Roan", "'Good Luck, Babe!'"),
    ("SZA", "'Saturn'"),
    ("Doja Cat", "'Paint the Town Red'"),
    ("Taylor Swift featuring Post Malone", "'Fortnight'"),
    ("Luke Combs", "'Fast Car'"),
    ("Tyla", "'Water'"),
    ("Sabrina Carpenter", "'Feather'"),
    ("Ariana Grande", "'We Can't Be Friends (Wait for Your Love)'"),
    ("Dasha", "'Austin'"),
    ("Morgan Wallen", "'Last Night'"),
    ("Morgan Wallen featuring Ernest", "'Cowgirls'"),
    ("Zach Bryan", "'Pink Skies'"),
    ("Morgan Wallen", "'Thinkin' Bout Me'"),
    ("Beyoncé", "'Texas Hold 'Em'"),
    ("Taylor Swift", "'Is It Over Now?'"),
    ("Marshmello and Kane Brown", "'Miles on It'"),
    ("Taylor Swift", "'I Can Do It with a Broken Heart'"),
    ("Jessie Murph and Jelly Roll", "'Wild Ones'"),
    ("Luke Combs", "'Ain't No Love in Oklahoma'"),
    ("¥$ (Kanye West and Ty Dolla Sign) featuring Rich the Kid and Playboi Carti", "'Carnival'"),
    ("Eminem", "'Houdini'"),
    ("GloRilla and Megan Thee Stallion", "'Wanna Be'"),
    ("Benson Boone", "'Slow It Down'"),
    ("Savage", "'Redrum'"),
    ("Dua Lipa", "'Houdini'"),
    ("GloRilla", "'Yeah Glo!'"),
    ("Drake featuring Sexyy Red and SZA", "'Rich Baby Daddy'"),
    ("Billie Eilish", "'What Was I Made For?'"),
    ("Djo", "'End of Beginning'"),
    ("Billie Eilish", "'Lunch'"),
    ("Flo Milli", "'Never Lose Me'"),
    ("Morgan Wallen", "'Lies Lies Lies'"),
    ("Future, Metro Boomin, Travis Scott, and Playboi Carti", "'Type Shit'"),
    ("FloyyMenor and Cris MJ", "'Gata Only'"),
    ("Chappell Roan", "'Hot to Go!'"),
    ("Mariah Carey", "'All I Want for Christmas Is You'"),
    ("Sexyy Red", "'Get It Sexyy'"),
    ("Muni Long", "'Made for Me'"),
    ("Olivia Rodrigo", "'Vampire'"),
    ("Bryson Tiller", "'Whatever She Wants'"),
    ("Brenda Lee", "'Rockin' Around the Christmas Tree'"),
    ("Warren Zeiders", "'Pretty Little Poison'"),
    ("Drake featuring J. Cole", "'First Person Shooter'"),
    ("Lady Gaga and Bruno Mars", "'Die with a Smile'"),
    ("Artemas", "'I Like the Way You Kiss Me'"),
    ("Jelly Roll", "'Need a Favor'"),
    ("Jelly Roll featuring Lainey Wilson", "'Save Me'"),
    ("Kendrick Lamar", "'Euphoria'"),
    ("Hardy", "'Truck Bed'"),
    ("Bobby Helms", "'Jingle Bell Rock'"),
    ("Miley Cyrus", "'Flowers'"),
    ("Luke Combs", "'Where the Wild Things Are'"),
    ("Nicki Minaj featuring Lil Uzi Vert", "'Everybody'"),
    ("Xavi", "'La Diabla'"),
    ("Myles Smith", "'Stargazing'"),
    ("Wham!", "'Last Christmas'"),
    ("Jelly Roll", "'I Am Not Okay'"),
    ("Post Malone featuring Blake Shelton", "'Pour Me a Drink'"),
    ("Chris Stapleton", "'White Horse'"),
    ("Paul Russell", "'Lil Boo Thang'"),
    ("Usher, Summer Walker and  Savage", "'Good Good'"),
    ("Batz and Drake", "'Act II: Date @ '"),
    ("Koe Wetzel featuring Jessie Murph", "'High Road'"),
    ("Bad Bunny", "'Monaco'"),
    ("Drake featuring Yeat", "'IDGAF'"),
    ("Parker McCollum", "'Burn It Down'"),
    ("Gunna", "'FukUMean'"),
    ("Sabrina Carpenter", "'Taste'"),
    ("Bailey Zimmerman", "'Where It Ends'"),
    ("Nicki Minaj", "'FTCU'"),
    ("Billie Eilish", "'Wildflower'"),
    ("Nate Smith", "'World on Fire'"),
    ("Victoria Monét", "'On My Mama'"),
    ("Ariana Grande", "'Yes, And?'"),
    ("Tate McRae", "'Exes'"),
    ("Burl Ives", "'A Holly Jolly Christmas'"),
    ("Tucker Wetmore", "'Wind Up Missin' You'"),
    ("Nate Smith", "'Bulletproof'"),
    ("Travis Scott featuring Playboi Carti", "'Fe!n'"),
    ("Cody Johnson", "'The Painter'"),
    ("Taylor Swift", "'Down Bad'"),
    ("Dua Lipa", "'Dance the Night'"),
]

def get_lyrics_from_ovh(artist, title, retries=3, delay=2):
    """Fetches lyrics from the lyrics.ovh API."""
    url = API_URL.format(artist=artist, title=title)
    print(f"Attempting to fetch lyrics for: {title} by {artist} from {url}")
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # Check if the response is valid JSON
            if 'application/json' in response.headers.get('Content-Type', ''):
                data = response.json()
                if 'lyrics' in data:
                    # Basic cleaning: replace multiple newlines and strip whitespace
                    lyrics = data['lyrics'].replace('\r\n', '\n').strip()
                    if lyrics: # Check if lyrics are not empty after stripping
                        print(f"Successfully fetched lyrics for: {title} by {artist}")
                        return lyrics
                    else:
                        print(f"API returned empty lyrics for: {title} by {artist}")
                        return None # Treat empty lyrics as not found
                else:
                    print(f"API response for '{title}' by {artist} did not contain 'lyrics' key.")
                    return None # Lyrics key missing
            else:
                # Handle cases where the API returns non-JSON (e.g., sometimes HTML error pages)
                print(f"Received non-JSON response for '{title}' by {artist}. Status: {response.status_code}")
                return None

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print(f"Lyrics not found (404) for: {title} by {artist}")
                return None # Song not found, stop retrying for this song
            else:
                print(f"HTTP error fetching lyrics for {title} by {artist}: {http_err} (Attempt {attempt + 1}/{retries})")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error fetching lyrics for {title} by {artist}: {req_err} (Attempt {attempt + 1}/{retries})")
        except json.JSONDecodeError:
             print(f"Failed to decode JSON response for {title} by {artist}. (Attempt {attempt + 1}/{retries})")
        except Exception as e:
            print(f"An unexpected error occurred for {title} by {artist}: {e} (Attempt {attempt + 1}/{retries})")


        if attempt < retries - 1:
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)

    print(f"Failed to fetch lyrics for {title} by {artist} after {retries} attempts.")
    return None

def save_lyrics(lyrics_data, output_file='data/lyrics_ovh.txt'):
    """Saves the fetched lyrics to a file."""
    os.makedirs('data', exist_ok=True)
    print(f"\nSaving lyrics to {output_file}...")
    count = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("LYRICS COLLECTION (Scraped from lyrics.ovh API)\n\n")
        for song_info, lyrics in lyrics_data.items():
            artist, title = song_info
            f.write(f"\n\n--- {title} by {artist} ---\n")
            f.write(lyrics)
            f.write("\n" + "="*50 + "\n")
            count += 1
    print(f"Successfully saved lyrics for {count} songs to {output_file}.")

if __name__ == "__main__":
    print("Starting lyrics scraper for lyrics.ovh...")
    fetched_lyrics = {}
    songs_not_found = []

    for artist, title in POP_SONGS:
        lyrics = get_lyrics_from_ovh(artist, title)
        if lyrics:
            fetched_lyrics[(artist, title)] = lyrics
        else:
            songs_not_found.append(f"{title} by {artist}")
        time.sleep(1) # add a small delay between requests

    if fetched_lyrics:
        save_lyrics(fetched_lyrics)
    else:
        print("\nNo lyrics were successfully fetched.")

    if songs_not_found:
        print("\nCould not find lyrics for the following songs:")
        for song in songs_not_found:
            print(f"- {song}")

    print("\nScraping finished.")