import requests
import json
import time
import os

API_URL = "https://api.lyrics.ovh/v1/{artist}/{title}"

def clean_artist_name(artist):
    """Clean artist name by removing featuring/and sections."""
    if ' featuring ' in artist.lower():
        return artist.split(' featuring ')[0].strip()
    if ', ' in artist.lower():
        return artist.split(', ')[0].strip()
    if ' and ' in artist:
        return artist.split(' and ')[0].strip()
    return artist

def get_lyrics_from_ovh(artist, title, retries=3, delay=2):
    """Fetches lyrics from the lyrics.ovh API with support for featured artists."""
    
    # First attempt: Try with cleaned artist name
    clean_artist = clean_artist_name(artist)
    
    # If the artist name was modified, try both versions
    attempts = [(clean_artist, title)]
    if clean_artist != artist and ' featuring ' in artist.lower():
        featured = artist.split(' featuring ')[1].strip()
        new_title = f"{title} (feat. {featured})"
        attempts.append((clean_artist, new_title))

    # Try each artist/title combination
    for attempt_artist, attempt_title in attempts:
        url = API_URL.format(artist=attempt_artist, title=attempt_title)
        print(f"Attempting to fetch lyrics for: {attempt_title} by {attempt_artist} from {url}")
        
        for retry in range(retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    if 'lyrics' in data:
                        lyrics = data['lyrics'].replace('\r\n', '\n').strip()
                        if lyrics:
                            print(f"Successfully fetched lyrics for: {attempt_title} by {attempt_artist}")
                            return lyrics
                        else:
                            print(f"API returned empty lyrics for: {attempt_title} by {attempt_artist}")
                else:
                    print(f"Received non-JSON response for '{attempt_title}' by {attempt_artist}. Status: {response.status_code}")

            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 404:
                    print(f"Lyrics not found (404) for: {attempt_title} by {attempt_artist}")
                    break  # Try next artist/title combination if available
                else:
                    print(f"HTTP error fetching lyrics for {attempt_title} by {attempt_artist}: {http_err} (Attempt {retry + 1}/{retries})")
            except requests.exceptions.RequestException as req_err:
                print(f"Request error fetching lyrics for {attempt_title} by {attempt_artist}: {req_err} (Attempt {retry + 1}/{retries})")
            except json.JSONDecodeError:
                print(f"Failed to decode JSON response for {attempt_title} by {attempt_artist}. (Attempt {retry + 1}/{retries})")
            except Exception as e:
                print(f"An unexpected error occurred for {attempt_title} by {attempt_artist}: {e} (Attempt {retry + 1}/{retries})")

            if retry < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)

    print(f"Failed to fetch lyrics for {title} by {artist} after all attempts.")
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