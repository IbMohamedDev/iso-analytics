import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from string import ascii_lowercase as alp



def scrape_player_bio():
    players_data = []
    for ch in alp:
        url = f"https://www.basketball-reference.com/players/{ch}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the player table
        table = soup.find('div', id='div_players')
        
    
 
    # Get all rows from the table body
        rows = table.find('tbody').find_all('tr')
    
    # Extract data from each row
        for row in rows:
            player = row.find('th', {'data-stat': 'player'})
            bball_id = player.get('data-append-csv')
            year_from = row.find('td', {'data-stat': 'year_min'}).text.strip()
            year_to = row.find('td', {'data-stat': 'year_max'}).text.strip()
            position = row.find('td', {'data-stat': 'pos'}).text.strip()
            height = row.find('td', {'data-stat': 'height'}).text.strip()
            weight = row.find('td', {'data-stat': 'weight'}).text.strip()
            birth_date = row.find('td', {'data-stat': 'birth_date'}).text.strip()
            
            # Handle college data - some players might not have college info
            college_td = row.find('td', {'data-stat': 'colleges'})
            college = college_td.text.strip() if college_td else None
            
            # Add data to list
            players_data.append({
                'Player': player.text,
                'From': year_from,
                'To': year_to,
                'Position': position,
                'Height': height,
                'Weight': weight,
                'Birth Date': birth_date,
                'College': college,
                'bball_id': bball_id
            })
        
        # Create DataFrame
    df = pd.DataFrame(players_data)
    df.to_csv('temp_bio.csv')
    print(df)

def scrape_draft_data(year):
   
    url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"

    
    try:
        # Send request to the URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Create BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing draft data
        table = soup.find('table', {'id': 'stats'})
        if not table:
            raise ValueError(f"Could not find the draft data table for year {year}")
            
        # Initialize lists to store data
        player_names = []
        draft_years = []
        draft_rounds = []
        draft_numbers = []
        
        # Process each row in the table
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            # Extract player name
            player_cell = row.find('td', {'data-stat': 'player'})
            if player_cell:
                player_names.append(player_cell.text.strip())
            
            # Extract draft number (pick overall)
            pick_cell = row.find('td', {'data-stat': 'pick_overall'})
            if pick_cell and pick_cell.text:
                pick_number = int(pick_cell.text)
                draft_numbers.append(pick_number)
                draft_rounds.append(1 if pick_number <= 30 else 2)
                draft_years.append(year)
        
        # Ensure all lists have the same length
        min_length = min(len(player_names), len(draft_years), len(draft_rounds), len(draft_numbers))
        
        # Create DataFrame
        df = pd.DataFrame({
            'Player': player_names[:min_length],
            'draft_year': draft_years[:min_length],
            'draft_round': draft_rounds[:min_length],
            'draft_number': draft_numbers[:min_length]
        })
        
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request for year {year}: {e}")
        return None
    except Exception as e:
        print(f"Error processing data for year {year}: {e}")
        return None

#this function gets called then saved to a csv. 
def get_all_draft_data(start_year=1955, end_year=1959):
   
    all_data = []
    
    for year in range(start_year, end_year + 1):
        print(f"Scraping data for year {year}...")
        df = scrape_draft_data(year)
        if df is not None:
            all_data.append(df)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        return combined_df
    return None


