import json
import pandas as pd
import numpy as np
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()


supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase credentials. Check .env file.")

supabase = create_client(supabase_url, supabase_key)



def load_players_data(filename='updated_players.csv'):
    """Load players data from CSV and return player_id mapping."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"CSV file '{filename}' not found.")
    
    df = pd.read_csv(filename)
    
    # Ensure necessary columns exist
    required_columns = {'Player', 'Team','From', 'To', 'Position', 'Height', 'Weight', 'Birth Date', 'College', 'draft_year', 'draft_round', 'draft_number', 'bball_id'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {missing_columns}")
    
    # Convert date field safely
    df['birth_date'] = pd.to_datetime(df['Birth Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # Clean data using applymap
    df = df.where(pd.notna(df), None)

    players_data = []
    for _, row in df.iterrows():
        player = {
            'player': row['Player'],
            'from': row['From'],
            'to': row['To'],
            'position': row['Position'] if pd.notna(row['Position']) else None,
            'height': row['Height'] if pd.notna(row['Height']) else None,
            'weight': float(row['Weight']) if pd.notna(row['Weight']) else None,
            'birth_date': row['birth_date'] if pd.notna(row['birth_date']) else None,
            'colleges': row['College'] if pd.notna(row['College']) else None,
            'player_id': row['bball_id'] if pd.notna(row['bball_id']) else None,
            'draft_year': int(row['draft_year']) if pd.notna(row['draft_year']) else None,
            'draft_round': int(row['draft_round']) if pd.notna(row['draft_round']) else None,
            'draft_number': int(row['draft_number']) if pd.notna(row['draft_number']) else None,
             'team': row['Team'],
        }
        players_data.append(player)
        #print(json.dumps(players_data[:5], indent=2))  # Print first 5 entries for debugging

    players_data = list({player["player_id"]: player for player in players_data}.values())

    # Insert players and get their IDs
    #result = supabase.table("player").upsert(players_data).execute()
    result = supabase.table("player").upsert(players_data, on_conflict=["player_id"]).execute()


    
    # Create mapping of player names to their IDs
    player_mapping = {df.iloc[i]['Player']: player['id'] for i, player in enumerate(result.data)}

    return player_mapping




def load_awards_data(filename='backend/data/updated_awards_full.csv'):
    """Load awards data from CSV and return a list of award records."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"CSV file '{filename}' not found.")
    
    df = pd.read_csv(filename)
  
    required_columns = {'Season', 'Award', 'bball_id'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing columns in CSV: {missing_columns}")
    
    
    df['Season'] = df['Season'].astype(str)
    df['Award'] = df['Award'].astype(str)
    df = df.where(pd.notna(df), None)

    awards_data = []
    for _, row in df.iterrows():
        award = {
            'season': row['Season'],
            'award': row['Award'],
            'player_id' : row['bball_id']
        }
        awards_data.append(award)
        

    result = supabase.table("awards").upsert(awards_data, on_conflict=[ "id"]).execute()
    

    return awards_data
    
    
    
def load_stats(filename,stats_type):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"CSV file '{filename}' not found.")
        
        df = pd.read_csv(filename)
       
        required_columns = {'Player_id','G','PTS','TRB','AST','FG%','FG3%','FT%','eFG%','PER','WS'}

        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing columns in CSV: {missing_columns}")
        
     
        df.replace('-', None, inplace=True)  
        df = df.where(pd.notna(df), None)  


        stats_data = []
        
        for _, row in df.iterrows():
            stat = {
                'player_id': row['Player_id'],
                'g': int(row['G']) if pd.notna(row['G']) else None,  # Ensure it's an integer
                'pts': float(row['PTS']) if pd.notna(row['PTS']) else None,
                'trb': float(row['TRB']) if pd.notna(row['TRB']) else None,
                'ast': float(row['AST']) if pd.notna(row['AST']) else None,
                'fg_per': float(row['FG%']) if pd.notna(row['FG%']) else None,
                'fg3_per': float(row['FG3%']) if pd.notna(row['FG3%']) else None,
                'ft_per': float(row['FT%']) if pd.notna(row['FT%']) else None,
                'efg_per': float(row['eFG%']) if pd.notna(row['eFG%']) else None,
                'per': float(row['PER']) if pd.notna(row['PER']) else None,
                'ws': float(row['WS']) if pd.notna(row['WS']) else None,
            }
            
            stats_data.append(stat)
          
        result = supabase.table(stats_type).upsert(stats_data, on_conflict=[ "id"]).execute()
        

        return stats_data
    
    
def combine_bio_draft_data():
  
    file_path = 'backend/data/'
    players_df = pd.read_csv('Player.csv').drop(['Team'], axis=1)
    teams_df = pd.read_csv('player_team.csv').drop(['Unnamed: 0'],axis=1)
    #print(players_df)
    
    #player_df2 = pd.merge(players_df,teams_df, on='Player')
    player_df2 = players_df.merge(teams_df, on="Player", how="left")
    #player_df2.fillna("Unknown", inplace=True)
    player_df2.to_csv('updated_players.csv', index=False)
    print(player_df2)
    #pd.merge(df, df2, on=['Player', 'Season', 'Award', 'Team'], how='outer')
    
    # file_path = 'backend/data/'
    # champ_df = pd.read_csv(file_path+'championships.csv')
    # awards_df = pd.read_csv(file_path+'awards_final.csv')
    
    
    # champ_df.drop('Player_id', axis=1, inplace=True)
    # awards_df.drop('Unnamed: 0', axis=1, inplace=True)
    # awards_df.drop('Unnamed: 0.1', axis=1, inplace=True)

    # merged_awards_df = pd.concat([awards_df,champ_df])


    # #removing NaN values 
    # awards_df2 = merged_awards_df.where(pd.notnull(merged_awards_df), None)
   
    
    
    # players_df = pd.read_csv('Player.csv')
    
    # #players_df.drop(['Team', 'From', 'To', 'draft_year', 'draft_round', 'draft_number'], axis=1, inplace=True)
    # player_ids = players_df[['Player','bball_id']]
    # player_ids.to_csv('player_ids.csv', index=False)

    # awards_df2 = pd.merge(awards_df2,player_ids, on='Player')
    # print(awards_df2)
    # awards_df2.to_csv('updated_awards_full.csv')
    
#combine_bio_draft_data()

# def combine_csv_data():
#     df = pd.read_csv('Player_awards.csv')
#     df2 = pd.read_csv('backend/data/all_nba_final.csv')

#     # Merge awards data
#     merged_awards_df = pd.merge(df, df2, on=['Player', 'Season', 'Award', 'Team'], how='outer')

#     df3 = pd.read_csv('Player.csv')

#    # Drop the 'Unnamed' column
#     awards_df = merged_awards_df.drop(columns=["Unnamed: 0"], errors="ignore")
#     #awards_df = merged_awards_df.drop(columns=["Team"], errors="ignore")

#     print(awards_df)

#     # Clean player names in awards dataset (remove extra quotes and spaces)
#     #awards_df["Player"] = awards_df["Player"].str.replace(r'[^a-zA-Z\s]', '', regex=True).str.strip()

#     # Merge awards with player dataset to add 'bball_id'
#     awards_df = awards_df.merge(df3[['Player', 'bball_id']], on="Player", how="left")

#     # Save or display
#     awards_df.to_csv("cleaned_awards.csv", index=False)
#     #print(awards_df)
        
#combine_bio_draft_data()

def main():
    try:
        #print("Loading players data...")
        player_mapping = load_players_data()
        #print("Database setup complete!")
        
        #awards_mapping = load_awards_data()
        
        #stats = load_stats('backend/data/season_stats.csv', 'current_stats')
        print('')
        # combine_csv_data()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()