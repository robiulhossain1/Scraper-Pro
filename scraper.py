import re
import time
import requests
from bs4 import BeautifulSoup


def update_playlist():
    
    url = "https://toffeelive.com/en/live" 

    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    
    response = requests.get(url, headers=headers)

    
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    
    soup = BeautifulSoup(response.text, 'html.parser')

    
    m3u8_urls = list(
        set(
            url for url in re.findall(r'https://[^"]+\.m3u8', response.text)
            if "bldcmprod-cdn.toffeelive.com" in url
        )
    )

    
    cookie_match = re.search(r'Edge-Cache-Cookie=([^;\\]+)', response.text)
    edge_cache_cookie = f"Edge-Cache-Cookie={cookie_match.group(1)}" if cookie_match else "Edge-Cache-Cookie=Not Available"

    
    playlist_file = 'playlist.m3u'

    
    with open(playlist_file, 'w') as f:
        
        f.write("#EXTM3U\n")

        
        for m3u8_url in m3u8_urls:
            
            channel_name = m3u8_url.split('/')[-2].replace('_', ' ').title()  

            
            f.write(f"#EXTINF:-1, {channel_name}\n")

            
            user_agent = "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64103898/4d2ec9b8c7534adc"
            f.write(f"#EXTVLCOPT:http-user-agent={user_agent}\n")

            
            f.write(f"#EXTHTTP:{{\"cookie\":\"{edge_cache_cookie}\"}}\n")

            
            f.write(f"{m3u8_url}\n")

    print(f"M3U playlist created and saved to '{playlist_file}'.")


while True:
    update_playlist()  
    time.sleep(2400)  


