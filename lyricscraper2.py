import requests
import json
import time
import os

# Define the API endpoint
API_URL = "https://api.lyrics.ovh/v1/{artist}/{title}"

# List of pop songs to fetch lyrics for (artist, title)
# Feel free to modify this list!
POP_SONGS = [
    ("Taylor Swift", "Blank Space"),
    ("Ed Sheeran", "Shape of You"),
    ("Katy Perry", "Roar"),
    ("Bruno Mars", "Uptown Funk"),
    ("Lady Gaga", "Bad Romance"),
    ("Rihanna", "Umbrella"),
    ("Justin Bieber", "Sorry"),
    ("Ariana Grande", "Thank U, Next"),
    ("Maroon 5", "Sugar"),
    ("Coldplay", "Yellow") # Example of a song potentially not found on this API
]

def get_lyrics_from_ovh(artist, title, retries=3, delay=2):
    """Fetches lyrics from the lyrics.ovh API."""
    url = API_URL.format(artist=artist, title=title)
    print(f"Attempting to fetch lyrics for: {title} by {artist} from {url}")
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10) # Add a timeout
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
                # You might want to inspect response.text here if debugging
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
             # Maybe inspect response.text here
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
        time.sleep(1) # Be respectful to the API, add a small delay between requests

    if fetched_lyrics:
        save_lyrics(fetched_lyrics)
    else:
        print("\nNo lyrics were successfully fetched.")

    if songs_not_found:
        print("\nCould not find lyrics for the following songs:")
        for song in songs_not_found:
            print(f"- {song}")

    print("\nScraping finished.")