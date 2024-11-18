import re
import time
import requests
from bs4 import BeautifulSoup

# Function to scrape and update the M3U playlist
def update_playlist():
    # Define the target URL
    url = "https://toffeelive.com/en/live"  # Replace with your actual URL

    # Set up headers for the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all text matching m3u8 URLs
    m3u8_urls = list(
        set(
            url for url in re.findall(r'https://[^"]+\.m3u8', response.text)
            if "bldcmprod-cdn.toffeelive.com" in url
        )
    )

    # Extract the full Edge-Cache-Cookie with its prefix
    cookie_match = re.search(r'Edge-Cache-Cookie=([^;\\]+)', response.text)
    edge_cache_cookie = f"Edge-Cache-Cookie={cookie_match.group(1)}" if cookie_match else "Edge-Cache-Cookie=Not Available"

    # Define the M3U playlist filename
    playlist_file = 'playlist.m3u'

    # Open the playlist file to write
    with open(playlist_file, 'w') as f:
        # Add M3U header
        f.write("#EXTM3U\n")

        # Loop through the m3u8 URLs and write them to the M3U file
        for m3u8_url in m3u8_urls:
            # Extract channel name from the m3u8 URL (last part before '/playlist.m3u8')
            channel_name = m3u8_url.split('/')[-2].replace('_', ' ').title()  # Convert underscores to spaces and capitalize

            # Construct the EXTINF line with the extracted channel name
            f.write(f"#EXTINF:-1, {channel_name}\n")

            # Construct the EXTVLCOPT line for the user-agent
            user_agent = "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc"
            f.write(f"#EXTVLCOPT:http-user-agent={user_agent}\n")

            # Construct the EXTHHTP line with the cookie
            f.write(f"#EXTHTTP:{{\"cookie\":\"{edge_cache_cookie}\"}}\n")

            # Write the m3u8 URL
            f.write(f"{m3u8_url}\n")

    print(f"M3U playlist created and saved to '{playlist_file}'.")

# Infinite loop to run the script every 2 minutes
while True:
    update_playlist()  # Update the playlist
    time.sleep(2400)  # Wait for 2 minutes before running again


