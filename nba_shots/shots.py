# import asyncio
# import os
# import json
# import pandas as pd
# from playwright.async_api import async_playwright
# from bs4 import BeautifulSoup
# import aiofiles
# import random

# TIMEOUT = 20000  # 20s timeout
# USER_AGENT = (
#     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
#     "(KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
# )

# # Read player IDs
# player_ids_df = pd.read_csv('updated_players.csv')
# player_ids = list(player_ids_df["player_id"])

# async def new_page(browser):
#     page = await browser.new_page()
#     await page.set_extra_http_headers({"User-Agent": USER_AGENT})
#     await page.set_viewport_size({"width": 1980, "height": 1080})
#     return page

# async def fetch_url(browser, url):
#     page = await new_page(browser)
#     await page.goto(url, timeout=TIMEOUT, wait_until="domcontentloaded")
#     html = await page.content()
#     await page.close()
#     return html

# async def download_shooting_data(browser, player_id):
#     """Downloads and saves the shooting data HTML for each player."""
#     url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}/shooting/2026"
#     html_filename = f"shots_{player_id}.html"

#     if os.path.exists(html_filename):
#         print(f"Skipping download for {player_id}, file already exists.")
#         return

#     retries = 3
#     delay = 3

#     for attempt in range(retries):
#         try:
#             print(f"Downloading HTML for {player_id} (Attempt {attempt + 1})...")
#             html = await fetch_url(browser, url)

#             async with aiofiles.open(html_filename, "w", encoding="utf-8") as f:
#                 await f.write(html)

#             print(f"Downloaded HTML for {player_id}.")
#             return

#         except Exception as e:
#             print(f"Error downloading for {player_id}: {e}")

#             if attempt == retries - 1:
#                 print(f"Skipping {player_id} after {retries} attempts.")
#                 return

#             backoff = random.uniform(delay, delay * 2)
#             print(f"Retrying in {backoff:.2f} seconds...")
#             await asyncio.sleep(backoff)

#         delay *= 2

# async def parse_shots(player_id):
#     """Parses the player's shooting data from their specific HTML file."""
#     print(f"Parsing shot data for {player_id}...")
#     html_filename = f"shots_{player_id}.html"

#     if not os.path.exists(html_filename):
#         print(f"Skipping {player_id}, HTML file not found.")
#         return None

#     async with aiofiles.open(html_filename, "r", encoding="utf-8") as f:
#         html = await f.read()

#     soup = BeautifulSoup(html, "html.parser")
#     shot_divs = soup.select(".shot-area > div")

#     shots = []
#     for div in shot_divs:
#         style = div.get("style", "")
#         classes = div.get("class", [])
#         tip = div.get("tip", "")

#         try:
#             x = int(style.split("left:")[1].split("px")[0].strip())
#             y = int(style.split("top:")[1].split("px")[0].strip())
#         except (IndexError, ValueError):
#             continue

#         made_shot = "make" in classes
#         shot_pts = 3 if "3-pointer" in tip else 2

#         shots.append({"x": x, "y": y, "madeShot": made_shot, "shotPts": shot_pts})

#     return {"playerId": player_id, "shots": shots} if shots else None

# async def main():
#     """Main function to download and parse shot data."""
#     print("Starting browser...")
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=True)

#         try:
#             # Step 1: Download HTML for each player with delay between requests
#             for player_id in player_ids:
#                 await download_shooting_data(browser, player_id)
#                 await asyncio.sleep(random.uniform(2, 5))

#             # Step 2: Parse HTML files into JSON
#             all_shots = []
#             for player_id in player_ids:
#                 shots_data = await parse_shots(player_id)
#                 if shots_data:
#                     all_shots.append(shots_data)

#             async with aiofiles.open("shots.json", "w", encoding="utf-8") as f:
#                 await f.write(json.dumps(all_shots, indent=2))

#         finally:
#             await browser.close()
#             print("Done!")

# if __name__ == "__main__":
#     asyncio.run(main())