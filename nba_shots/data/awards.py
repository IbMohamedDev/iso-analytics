import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_player_awards(url):
    """
    Scrapes NBA Defensive Player of the Year award data from Basketball Reference.
    Returns a pandas DataFrame with season, player, and team information.
    """
    
    
    try:
        # Fetch the page
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main table body
        tbody = soup.find('tbody')
        if not tbody:
            raise ValueError("Could not find table body in the page")
        
        # Initialize lists to store data
        seasons = []
        players = []
        teams = []
        h1 = soup.find('h1')
    
        if h1.text == 'NBA & ABA Rookie of the Year (Wilt Chamberlain Trophy) Award Winners':
            award = 'ROY'
        elif h1.text == 'NBA MVP & ABA Most Valuable Player Award Winners':
            award = 'MVP'
        elif h1.text == 'NBA Defensive Player of the Year (Hakeem Olajuwon Trophy) Award Winners':
            award = 'DPOY'
        elif h1.text == 'NBA Finals Most Valuable Player (Bill Russell Trophy) Award Winners':
            award = 'FMVP'
        else:
            award = None
        print(award)
    
        # Extract rows
        for row in tbody.find_all('tr'):
            
            # Get season
            season = row.find('th', {'data-stat': 'season'})
            if season:
                seasons.append(season.text)
            
            # Get player
            player = row.find('td', {'data-stat': 'player'})
            if player:
                players.append(player.text)
            
            # Get team
            team = row.find('td', {'data-stat': 'team_id'})
            if team:
                teams.append(team.text)
        
        # Create DataFrame
        awards_df = pd.DataFrame({
            'Season': seasons,
            'Player': players,
            'Team': teams, 
            'Award': award
        })
        
        return awards_df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def main():
    # Get the awards data
    #dpoy
    dpoy_url = 'https://www.basketball-reference.com/awards/dpoy.html'
    mvp_url = 'https://www.basketball-reference.com/awards/mvp.html'
    roy_url = 'https://www.basketball-reference.com/awards/roy.html'
    finals_mvp = 'https://www.basketball-reference.com/awards/finals_mvp.html'


    dpoy_df = get_player_awards(dpoy_url)
    roy_df = get_player_awards(roy_url)
    mvp_df = get_player_awards(mvp_url)
    finalsmvp_df = get_player_awards(finals_mvp)
    #concat all awards into one df 
    player_awards_df = pd.concat([dpoy_df, roy_df, mvp_df,finalsmvp_df], ignore_index=True)


        
    #  save to CSV
    file_path = 'backend/data/Player_awards.csv'
    player_awards_df.to_csv(file_path, index=False)
    #mvp_df.to_csv('mvp_awards.csv', index=False)


if __name__ == "__main__":
    main()
    
    
    
    