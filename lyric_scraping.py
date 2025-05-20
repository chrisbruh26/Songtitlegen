#!/usr/bin/env python3
"""
Improved Lyrics Scraper
Scrapes lyrics from Genius and other sources with better error handling and more songs
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import os
import re

# User agent list to rotate and avoid blocking
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
]

# Configuration
CONFIG = {
    'output_file': 'scraped_lyrics.txt',
    'backup_file': 'scraped_lyrics_backup.txt',
    'request_delay': 2,  # Delay between requests in seconds
    'max_retries': 3,    # Maximum number of retries for failed requests
    'timeout': 10,       # Request timeout in seconds
}

def get_random_user_agent():
    """Return a random user agent from the list"""
    return random.choice(USER_AGENTS)

def clean_lyrics(lyrics_text):
    """Clean up the lyrics text"""
    if not lyrics_text:
        return ""
    
    # Remove [Verse], [Chorus], etc. labels
    lyrics_text = re.sub(r'\[.*?\]', '', lyrics_text)
    
    # Remove extra whitespace
    lyrics_text = re.sub(r'\s+', ' ', lyrics_text).strip()
    
    # Remove non-lyrical content
    lyrics_text = re.sub(r'Lyrics from Genius\.com', '', lyrics_text, flags=re.IGNORECASE)
    
    return lyrics_text

def get_lyrics_from_genius(song_url, retries=0):
    """
    Scrape lyrics from a Genius song page with retry logic
    """
    if retries >= CONFIG['max_retries']:
        print(f"Maximum retries reached for {song_url}")
        return None
    
    headers = {'User-Agent': get_random_user_agent()}
    
    try:
        response = requests.get(song_url, headers=headers, timeout=CONFIG['timeout'])
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try different selectors for Genius lyrics
            selectors = [
                'div[class^="Lyrics__Container"]',  # Current Genius format
                'div.lyrics',                       # Older Genius format
                '.song_body-lyrics',                # Another possible format
            ]
            
            for selector in selectors:
                lyrics_container = soup.select_one(selector)
                if lyrics_container:
                    lyrics = lyrics_container.get_text(separator='\n')
                    return clean_lyrics(lyrics)
            
            print(f"Lyrics container not found for {song_url}")
            return None
            
        elif response.status_code == 429:  # Too Many Requests
            wait_time = random.uniform(5, 15)
            print(f"Rate limited. Waiting {wait_time:.2f} seconds before retry...")
            time.sleep(wait_time)
            return get_lyrics_from_genius(song_url, retries + 1)
            
        else:
            print(f"Failed to fetch page: status code {response.status_code}")
            return None
            
    except requests.RequestException as e:
        print(f"Request error: {e}")
        time.sleep(CONFIG['request_delay'])
        return get_lyrics_from_genius(song_url, retries + 1)

def backup_existing_lyrics():
    """Create a backup of the existing lyrics file if it exists"""
    if os.path.exists(CONFIG['output_file']):
        try:
            with open(CONFIG['output_file'], 'r', encoding='utf-8') as source:
                content = source.read()
            
            with open(CONFIG['backup_file'], 'w', encoding='utf-8') as backup:
                backup.write(content)
            
            print(f"Backup created: {CONFIG['backup_file']}")
        except Exception as e:
            print(f"Failed to create backup: {e}")

def scrape_song_lyrics(songs_to_scrape, append_mode=True):
    """
    Scrape lyrics from a list of song URLs
    
    Args:
        songs_to_scrape: List of song URLs to scrape
        append_mode: If True, append to existing file; if False, overwrite
    """
    # Create a backup if we're not in append mode
    if not append_mode and os.path.exists(CONFIG['output_file']):
        backup_existing_lyrics()
    
    # Open the output file in the appropriate mode
    file_mode = 'a' if append_mode else 'w'
    
    successful_scrapes = 0
    
    for song_url in songs_to_scrape:
        print(f"Scraping lyrics from: {song_url}")
        
        try:
            lyrics = get_lyrics_from_genius(song_url)
            
            if lyrics:
                with open(CONFIG['output_file'], file_mode, encoding='utf-8') as lyrics_file:
                    lyrics_file.write(lyrics + "\n\n")
                
                print(f"✓ Successfully scraped lyrics from {song_url}")
                successful_scrapes += 1
            else:
                print(f"✗ No lyrics found for {song_url}")
            
            # Add delay between requests to avoid rate limiting
            time.sleep(CONFIG['request_delay'])
            
        except Exception as e:
            print(f"Error processing {song_url}: {e}")
    
    print(f"\nScraping complete. Successfully scraped {successful_scrapes} out of {len(songs_to_scrape)} songs.")
    print(f"Lyrics saved to: {CONFIG['output_file']}")

def main():
    """Main function to run the lyrics scraper"""
    print("\n=== Improved Lyrics Scraper ===\n")
    
    # List of songs to scrape - add your favorite songs here!
    songs_to_scrape = [
        # Rock/Metal
        "https://genius.com/Fall-out-boy-the-mighty-fall-lyrics",
        "https://genius.com/Fall-out-boy-young-volcanoes-lyrics",
        "https://genius.com/Ice-nine-kills-stabbing-in-the-dark-lyrics",
        
        # Pop
        "https://genius.com/Halsey/new-americana-lyrics",
        "https://genius.com/Halsey/castle-lyrics",
        "https://genius.com/Halsey/hold-me-down-lyrics",
        "https://genius.com/Halsey/coming-down-lyrics",
        "https://genius.com/Halsey/angel-on-fire-lyrics",
        


        


     ]
    
    # Ask if user wants to append or overwrite
    append_mode = True
    if os.path.exists(CONFIG['output_file']):
        print(f"The file {CONFIG['output_file']} already exists.")
        choice = input("Do you want to append to this file? (y/n): ").lower()
        append_mode = choice.startswith('y')
    
    # Scrape the songs
    scrape_song_lyrics(songs_to_scrape, append_mode)

if __name__ == "__main__":
    main()
