import asyncio
import os
import json
import pandas as pd
from pyppeteer import launch
from bs4 import BeautifulSoup
import aiofiles

TIMEOUT = 20000  # 20s timeout
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
)

# Read player IDs
player_ids_df = pd.read_csv('updated_players.csv')
filtered_players = player_ids_df[player_ids_df["To"] == 2025.0]
player_ids = list(filtered_players["player_id"])

async def new_page(browser):
    """Creates a new browser page with custom settings."""
    page = await browser.newPage()
    await page.setUserAgent(USER_AGENT)
    await page.setViewport({"width": 1980, "height": 1080})
    return page

async def fetch_url(browser, url):
    """Fetches a webpage and returns its HTML content."""
    page = await new_page(browser)
    await page.goto(url, {"timeout": TIMEOUT, "waitUntil": "domcontentloaded"})
    html = await page.content()
    await page.close()
    return html

async def download_shooting_data(browser, player_id):
    """Downloads and saves the shooting data HTML for each player."""
    url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}/shooting/2025"
    html_filename = f"shots_{player_id}.html"  # Unique filename per player

    if os.path.exists(html_filename):
        print(f"Skipping download for {player_id}, file already exists.")
        return

    print(f"Downloading HTML for {player_id}...")
    html = await fetch_url(browser, url)
    
    async with aiofiles.open(html_filename, "w", encoding="utf-8") as f:
        await f.write(html)

async def parse_shots(player_id):
    """Parses the player's shooting data from their specific HTML file."""
    print(f"Parsing shot data for {player_id}...")
    html_filename = f"shots_{player_id}.html"

    if not os.path.exists(html_filename):
        print(f"Skipping {player_id}, HTML file not found.")
        return None

    async with aiofiles.open(html_filename, "r", encoding="utf-8") as f:
        html = await f.read()

    soup = BeautifulSoup(html, "html.parser")
    shot_divs = soup.select(".shot-area > div")

    shots = []
    for div in shot_divs:
        style = div.get("style", "")
        classes = div.get("class", [])
        tip = div.get("tip", "")

        try:
            x = int(style.split("left:")[1].split("px")[0].strip())
            y = int(style.split("top:")[1].split("px")[0].strip())
        except (IndexError, ValueError):
            continue

        made_shot = "make" in classes
        shot_pts = 3 if "3-pointer" in tip else 2

        shots.append({"x": x, "y": y, "madeShot": made_shot, "shotPts": shot_pts})
    
    return {"playerId": player_id, "shots": shots} if shots else None

async def main():
    """Main function to download and parse shot data."""
    print("Starting browser...")
    browser = await launch()

    # Step 1: Download HTML for each player
    for player_id in player_ids:
        await download_shooting_data(browser, player_id)
    
    await browser.close()  # Close browser after downloading all files

    # Step 2: Parse HTML files into JSON
    all_shots = []
    for player_id in player_ids:
        shots_data = await parse_shots(player_id)
        if shots_data:  # Only add if parsing was successful
            all_shots.append(shots_data)  
             
    async with aiofiles.open("shots.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps(all_shots, indent=2))
    
    print("Done!")

asyncio.run(main())

