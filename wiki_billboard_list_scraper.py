import requests
from bs4 import BeautifulSoup
import json
import os

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

def scrape_billboard_songs(year):
    """
    Scrapes Billboard Year-End Hot 100 singles from Wikipedia for a specific year
    Returns a list of tuples containing (artist, title)
    """
    url = f"https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}"
    
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
        print(f"Error scraping Billboard songs for year {year}: {e}")
        return []

def save_songs_list(songs, year):
    """
    Saves the scraped songs list to a JSON file in the year_lists directory
    """
    os.makedirs('year_lists', exist_ok=True)
    output_file = f'year_lists/{year}_songs.json'
    
    try:
        with open(output_file, 'w') as file:
            json.dump(songs, file, indent=2)
        print(f"Successfully saved {len(songs)} songs to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving songs list: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python wiki_billboard_list_scraper.py <year>")
        sys.exit(1)
        
    year = sys.argv[1]
    print(f"Scraping Billboard Year-End Hot 100 singles for {year}...")
    songs = scrape_billboard_songs(year)
    
    if songs:
        print(f"Found {len(songs)} songs")
        save_songs_list(songs, year)
    else:
        print("No songs were found.")