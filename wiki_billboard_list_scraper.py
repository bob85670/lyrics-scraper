import requests
from bs4 import BeautifulSoup
import json

def clean_text(text):
    """
    Cleans and escapes text for Python string literals
    """
    # Remove citation brackets and numbers
    text = ''.join(char for char in text if char not in '[]0123456789')
    # Strip whitespace
    text = text.strip()
    # Replace double quotes with single quotes
    text = text.replace('"', "'")
    return text

def scrape_billboard_songs():
    """
    Scrapes Billboard Year-End Hot 100 singles from Wikipedia
    Returns a list of tuples containing (artist, title)
    """
    url = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_2024"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main rankings table
        table = soup.find('table', {'class': 'wikitable'})
        if not table:
            raise Exception("Could not find rankings table")
        
        songs = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            columns = row.find_all(['td', 'th'])
            if len(columns) >= 3:  # Ensure we have enough columns
                title = clean_text(columns[1].get_text())
                artist = clean_text(columns[2].get_text())
                if title and artist:
                    songs.append((artist, title))
        
        return songs
        
    except Exception as e:
        print(f"Error scraping Billboard songs: {e}")
        return []

def update_pop_songs_list(songs):
    """
    Updates the POP_SONGS list in lyricscraper.py with new songs
    """
    try:
        with open('lyricscraper.py', 'r') as file:
            content = file.read()
            
        # Format the new songs list
        songs_str = "[\n"
        for artist, title in songs:
            songs_str += f'    ("{artist}", "{title}"),\n'
        songs_str += "]"
        
        # Replace the existing POP_SONGS list
        import re
        new_content = re.sub(
            r'POP_SONGS = \[.*?\]',
            f'POP_SONGS = {songs_str}',
            content,
            flags=re.DOTALL
        )
        
        with open('lyricscraper.py', 'w') as file:
            file.write(new_content)
            
        print(f"Successfully updated POP_SONGS list with {len(songs)} songs")
        
    except Exception as e:
        print(f"Error updating POP_SONGS list: {e}")

if __name__ == "__main__":
    print("Scraping Billboard Year-End Hot 100 singles...")
    songs = scrape_billboard_songs()
    
    if songs:
        print(f"Found {len(songs)} songs")
        update_pop_songs_list(songs)
    else:
        print("No songs were found. The POP_SONGS list was not updated.")