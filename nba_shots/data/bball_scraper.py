import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
from typing import List
import logging
import datetime


class BasketballReferenceScraper:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
        ]
        self.base_url = "https://www.basketball-reference.com/players"
        self.all_career_stats = []
        self.current_season_stats = []
        self.player_team = []
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='basketball_scraper.log'
        )

    def get_headers(self):
        return {"User-Agent": random.choice(self.user_agents)}

    def get_player_url(self, player_id: str):
        return f"{self.base_url}/{player_id[0]}/{player_id}.html"

    def make_request(self, url: str):
        try:
            response = requests.get(url, headers=self.get_headers())
            response.raise_for_status()
            time.sleep(2)  # Respectful delay between requests
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None

    def parse_championships(self, soup: BeautifulSoup):
        championships_section = soup.find('ul', id='bling')
        if not championships_section:
            return 0

        championship_texts = [
            li.text for li in championships_section.find_all('li') 
            if 'NBA Champ' in li.text
        ]
        
        if not championship_texts:
            return 0

        total_championships = sum(
            int(match.group()) 
            for text in championship_texts 
            if (match := re.search(r'\d+', text))
        )
        
        return 1 if len(str(total_championships)) == 4 else total_championships

    def parse_team(self, soup: BeautifulSoup):
        """Extracts the player's team from the page."""
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            strong_tag = p.find('strong')
            if strong_tag and strong_tag.text == 'Team':
                team_link = p.find('a')
                if team_link:
                    return team_link.text  # Return the team name

        return "Unknown"  # Default if no team is found

    def parse_career_stats(self, soup: BeautifulSoup, player_name: str, player_id:str):
        career_stats = {'Player': player_name, 'Player_id': player_id}
        stats_container = soup.find("div", class_="stats_pullout")
        
        if not stats_container:
            return career_stats

        for section in stats_container.find_all("div", class_=lambda x: x and x.startswith('p')):
            for stat_div in section.find_all("div", recursive=False):
                stat_name = stat_div.find("span", class_="poptip")
                if not stat_name:
                    continue
                    
                stat_name = stat_name.find("strong").text
                values = stat_div.find_all("p")
                
                if len(values) >= 2:
                    career_stats[stat_name] = values[1].text

        return career_stats

    def create_championships_df(self, player_name: str, num_champs: int, player_id: str):
        return pd.DataFrame({
            'Season': [None] * num_champs,
            'Player': [player_name] * num_champs,
            'Tm': [None] * num_champs,
            'Award': ['NBA Champion'] * num_champs,
            'Player_id': player_id
        })

    def scrape_player(self, player_id: str, last_year):
        url = self.get_player_url(player_id)
        response = self.make_request(url)
        
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        player_name = soup.find("h1")
        
        if not player_name:
            logging.error(f"Could not find player name for {player_id}")
            return None
            
        player_name = player_name.text.strip()
        print(f"Scraping: {player_name}")

        # Get team
        team = self.parse_team(soup)  # Call parse_team function
        self.player_team.append({'Player': player_name, 'Team':team})
        #print(self.player_team)

        # Get career stats
        career_stats = self.parse_career_stats(soup, player_name, player_id)
        #career_stats['Team'] = team  # Add team info to career stats
        self.all_career_stats.append(career_stats)

        # Get current season stats if player is active
        current_year = datetime.date.today().year
        if last_year == current_year:
            season_stats = self.parse_season_stats(soup, player_name, player_id)
            self.current_season_stats.append(season_stats)
            logging.info(f"Retrieved current season stats for {player_name}")

        # Get championships
        num_champs = self.parse_championships(soup)
        championship_rows = self.create_championships_df(player_name, num_champs, player_id)

        return championship_rows

    def scrape_players(self, player_ids: List[str], player_last_years):
        all_championships = []
        
        for player_id, last_year in zip(player_ids, player_last_years):
            try:
                logging.info(f"Scraping data for player: {player_id}")
                championship_data = self.scrape_player(player_id, last_year)
                if championship_data is not None:
                    all_championships.append(championship_data)
            except Exception as e:
                logging.error(f"Error scraping player {player_id}: {str(e)}")
                continue
    
        if not all_championships:
            logging.warning("No championship data was collected")
            return None
        
        try:
            final_championships = pd.concat(all_championships, ignore_index=True)
            career_stats_df = pd.DataFrame(self.all_career_stats)
            season_stats_df = pd.DataFrame(self.current_season_stats)

            # Save CSV files
            final_championships.to_csv('championships.csv', index=False)
            career_stats_df.to_csv('career_stats.csv', index=False)
            season_stats_df.to_csv('season_stats.csv', index=False)

            return final_championships
        
        except Exception as e:
            logging.error(f"Error processing or saving data: {str(e)}")
            return None

    def parse_season_stats(self, soup: BeautifulSoup, player_name: str, player_id: str):
        season_stats = {'Player': player_name, 'Player_id': player_id}
        stats_container = soup.find("div", class_="stats_pullout")
        
        if not stats_container:
            return 
        
        for section in stats_container.find_all("div", class_=lambda x: x and x.startswith('p')):
            for stat_div in section.find_all("div", recursive=False):
                stat_name = stat_div.find("span", class_="poptip").find("strong").text
                values = stat_div.find_all("p")
                if len(values) >= 2:
                    season_stats[stat_name] = values[0].text

        return season_stats


def main():
    # Read player IDs from CSV
    players_df = pd.read_csv('Player.csv')
    player_ids = players_df['bball_id'].tolist()
    player_last_years = players_df['To']
    

    # Initialize and run scraper
    scraper = BasketballReferenceScraper()
    championship_data = scraper.scrape_players(player_ids,player_last_years)
    
    
    #team
    
    team_df = pd.DataFrame(scraper.player_team)
    print(team_df)
    team_csv = team_df.to_csv('player_team.csv')
    
    
    
    
    logging.info("Scraping completed successfully")
    return championship_data

if __name__ == "__main__":
    main()