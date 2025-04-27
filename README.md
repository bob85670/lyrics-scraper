# Lyrics Scraper

> This repository allows you to use wiki "Billboard Year-End Hot 100 singles" song list and scrape songs in lyrics.ovh and store them in a text file.

The LyricsGenius API is no longer workable. See https://github.com/johnwmillr/LyricsGenius/issues/220. So LyricsGenius is deprecated.

## Usage

- For batch processing by year(s):
  - Single year: `python3 main.py 2022 2022`
  - Multiple years: `python3 main.py 2022 2023`
  Output will be saved to `data/lyrics{year}.txt`

- For individual song lookup:
  - Format: `python3 ovh_lyrics_scraper.py "Song Title" "Artist Name"`
  - Example: `python3 ovh_lyrics_scraper.py Flowers 'Miley Cyrus'`
  Output will be saved to the data directory
  
## License

[MIT](https://github.com/stanleycyang/lyrics-scraper/blob/master/LICENSE)