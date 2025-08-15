import re
from bs4 import BeautifulSoup
import pandas as pd
import requests


urls = [
    ('https://www.basketball-reference.com/awards/all_league.html', 'All-NBA'),
    ('https://www.basketball-reference.com/awards/all_defense.html', 'All-Defensive')
]



players = []
seasons = []


def get_allnba_data(page, award):
    # Find all rows in the table
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('tr')
    players = []
    all_nba = []
    
    #print(rows)
    for row in rows:
        #print(r)
        season = row.find('th', {"data-stat":"season"})
        if season is None:
            continue
        season = season.text.strip()
        #print(season.text)
        #print(r.find('td', {"data-stat":1}))
        for i in range(1,6):
            player = row.find('td', {"data-stat": i})
            if player is not None:
                name = player.text.strip()
                player_name = re.sub(r'\s[C|F|G]$', '', name)
                #print(player.text)
                if player_name:  # Only add if player name exists
                    all_nba.append({
                        'Season': season,
                        'Player': player_name,
                        'Team': None,
                        'Award': award
                    })
    
        df = pd.DataFrame(all_nba)
       
        
    return df
        
        

def main():
    awards = []
    #all-nba
    for url, award in urls:
        page = requests.get(url)
        df = get_allnba_data(page, award)
        awards.append(df)
    
    final_all_nba_df = pd.concat(awards, ignore_index=True) 
    final_all_nba_csv = final_all_nba_df.to_csv('all_nba_final.csv')
    

    
    
if __name__ == '__main__':
    main()
