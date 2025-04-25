# PYTHON GENIUS SCRAPER

import requests
from bs4 import BeautifulSoup
import os
import time
from fake_useragent import UserAgent

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

GENIUS_API_KEY = os.environ.get('GENIUS_API_KEY')

base_url = 'http://api.genius.com'
headers = {
    'Authorization': 'Bearer ' + GENIUS_API_KEY
}

# list of artists to scrape from
artists = [
            'Britney Spears',
            'Queen',
            'OneRepublic',
            'Whitney Houston',
            'Stevie Wonder',
            'Bon Jovi',
            'Avril Lavigne',
            'Carly Rae Jepsen',
            'David Bowie',
            'Amy Winehouse',
            'Christina Aguilera',
            'Gwen Stefani',
            'Coldplay',
            'Frank Sinatra',
            'Celine Dion',
            'Backstreet Boys',
            'Janet Jackson',
            'Jennifer Lopez',
            'Meghan Trainor',
            'Ellie Goulding',
            'Nelly Furtado',
            'Justin Bieber',
            'Katy Perry',
            'Bruno Mars',
            'Beyonce',
            'Lorde',
            'The Weeknd',
            'John Legend',
            'Rihanna',
            'Lady Gaga',
            'Usher',
            'Miley Cyrus',
            'Taylor Swift',
            'Major Lazer',
            'One Direction',
            'Ed Sheeran',
            'Sia',
            'Ariana Grande',
            'Calvin Harris',
            'Mariah Carey',
            'Madonna',
            'Elton John',
            'The Beatles',
            'Michael Jackson',
            'Bee Gees',
            'Prince',
            'Maroon 5',
            'The Black Eyed Peas',
            'P!NK',
            'TLC',
            'R. Kelly',
            'Kelly Clarkson',
            'Justin Timberlake',
            'Alessia Cara',
            'Shawn Mendes',
            'Hailee Steinfeld',
            'Jason Derulo',
            'Adele',
            'Zedd',
            'Train',
            'Selena Gomez',
            'Kygo',
        ]

def get_lyrics(song_api_path):
    try:
        song_url = base_url + song_api_path
        response = requests.get(song_url, headers=headers)
        json = response.json()

        path = json['response']['song']['path']
        #print('Path %s' % path)
        page_url = 'http://genius.com' + path

        # Add delay to avoid rate limiting
        time.sleep(2)
        
        # Use rotating user agents to appear more like a browser
        ua = UserAgent()
        page_headers = {
            'User-Agent': ua.random
        }
        
        # Get the page content
        page = requests.get(page_url, headers=page_headers)
        html = BeautifulSoup(page.text, 'html.parser')
        
        # Try different possible lyrics div classes (Genius sometimes changes these)
        lyrics_div = html.find('div', class_='lyrics') or \
                    html.find('div', class_='Lyrics__Container-sc-1ynbvzw-6') or \
                    html.find('div', class_='SongPageGriddesktop-sc-1px5b71-0')
        
        if lyrics_div:
            # Clean up the lyrics text
            lyrics = lyrics_div.get_text().strip()
            
            # Save to file with song information
            with open('data/input.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n\n--- {json['response']['song']['title']} by {json['response']['song']['artist_names']} ---\n")
                f.write(lyrics)
                f.write("\n" + "="*50 + "\n")  # Separator between songs
            
            print(f"Successfully scraped: {json['response']['song']['title']}")
        else:
            print(f"Could not find lyrics for: {json['response']['song']['title']}")
            
    except Exception as e:
        print(f"Error getting lyrics: {str(e)}")

def search_songs():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Clear the input file before starting
    with open('data/input.txt', 'w', encoding='utf-8') as f:
        f.write("LYRICS COLLECTION\n\n")
    
    for artist_name in artists:
        try:
            print(f"\nSearching for songs by {artist_name}")
            search_url = base_url + '/search'
            search_params = {
                'q': artist_name,
                'per_page': 5  # Limit to top 5 songs per artist
            }
            
            response = requests.get(search_url, headers=headers, params=search_params)
            json = response.json()
            
            if 'response' in json and 'hits' in json['response']:
                for hit in json['response']['hits']:
                    if hit['result']['primary_artist']['name'].lower() == artist_name.lower():
                        get_lyrics(hit['result']['api_path'])
                        time.sleep(1)  # Delay between songs
            
            time.sleep(2)  # Delay between artists
            
        except Exception as e:
            print(f"Error searching for {artist_name}: {str(e)}")
            continue

if __name__ == "__main__":
    print("Starting lyrics scraper...")
    search_songs()
    print("\nScraping completed! Check data/input.txt for results.")