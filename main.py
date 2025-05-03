import os
import json
import sys
from wiki_billboard_list_scraper import scrape_billboard_songs, save_songs_list
from ovh_lyrics_scraper import get_lyrics_from_ovh, save_lyrics

def process_year(year):
    """Process a single year: scrape Billboard list and fetch lyrics"""
    print(f"\nProcessing year {year}...")
    
    # Step 1: Scrape Billboard list
    print(f"Scraping Billboard Hot 100 for {year}...")
    songs = scrape_billboard_songs(year)
    if not songs:
        print(f"No songs found for year {year}")
        return
    
    # Save the Billboard list
    save_songs_list(songs, year)
    
    # Step 2: Fetch lyrics for each song
    print(f"\nFetching lyrics for {len(songs)} songs from {year}...")
    fetched_lyrics = {}
    songs_not_found = []
    
    for artist, title in songs:
        lyrics = get_lyrics_from_ovh(artist, title)
        if lyrics:
            fetched_lyrics[(artist, title)] = lyrics
        else:
            songs_not_found.append(f"{title} by {artist}")
    
    # Step 3: Save lyrics to year-specific file
    if fetched_lyrics:
        output_file = f'lyrics_data/lyrics_{year}.txt'
        save_lyrics(fetched_lyrics, output_file)
    else:
        print(f"\nNo lyrics were successfully fetched for {year}")
    
    if songs_not_found:
        print(f"\nCould not find lyrics for {len(songs_not_found)} songs from {year}:")
        for song in songs_not_found[:10]:  # Show first 10 missing songs
            print(f"- {song}")
        if len(songs_not_found) > 10:
            print(f"... and {len(songs_not_found) - 10} more")
        # Write missing lyrics to txt in project root, grouped by year
        with open("missing_lyrics.txt", "a", encoding="utf-8") as f:
            f.write(f"===== Year {year} =====\n")
            for song in songs_not_found:
                f.write(song + "\n")
            f.write("\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <start_year> <end_year>")
        print("Example: python main.py 2010 2022")
        sys.exit(1)
    
    try:
        start_year = int(sys.argv[1])
        end_year = int(sys.argv[2])
        
        if start_year > end_year:
            print("Error: Start year must be less than or equal to end year")
            sys.exit(1)
            
        if start_year < 1950 or end_year > 2024:
            print("Error: Years must be between 1950 and 2024")
            sys.exit(1)
        
        # Create necessary directories
        os.makedirs('year_lists', exist_ok=True)
        os.makedirs('lyrics_data', exist_ok=True)
        
        print(f"Starting lyrics scraping process for years {start_year} to {end_year}")
        
        # Process each year
        for year in range(start_year, end_year + 1):
            process_year(year)
            
        print("\nScraping process completed!")
        print(f"JSON files can be found in the 'year_lists' directory")
        print(f"Lyrics files can be found in the 'lyrics_data' directory")
        
    except ValueError:
        print("Error: Years must be valid numbers")
        sys.exit(1)

if __name__ == "__main__":
    main()