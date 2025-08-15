import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import { PlayerCard } from './PlayerCard'
import { ShotChart } from './ShotChart'
import {PlayerPercentiles} from './PlayerPercentiles'
import rapport_ranking from '../rapport_ranking'
    
export const Dashboard = () => {
    const { playerId } = useParams();
    const [playerData, setPlayerData] = useState();
    const [shotData, setShotData] = useState([]);
    const [currentPlayer, setCurrentPlayer] = useState();
  
    const apiUrl = import.meta.env.VITE_API_URL;

    useEffect(() => {
      const fetchPlayerData = async () => {
        try {
          const response = await fetch(`${apiUrl}/player/${playerId}`);
          const data = await response.json();
          
          console.log('API Response:', data); // Debug log
          console.log('Shot data from API:', data.shot_data); // Debug log
          
          let player_name = data.player.player;
          setCurrentPlayer(player_name);
          setPlayerData(data);
          
          // Fix: Use the entire shot_data array, not just the first element
          const shotDataArray = Array.isArray(data.shot_data) ? data.shot_data : [];
          console.log('Processed shot data:', shotDataArray); // Debug log
          setShotData(shotDataArray);
          
        } catch (error) {
          console.error('Failed to fetch player data:', error);
          setShotData([]); // Set empty array on error
        }
      };
  
      if (playerId) {
        fetchPlayerData();
      }
    }, [playerId, apiUrl]);
  
    // Get the player ranking from the rapport_ranking
    let playerRapport = rapport_ranking.find(player => player['Player'] === currentPlayer);
  
    return (
      <div className="flex flex-row">
        <PlayerCard playerId={playerId} playerData={playerData} />
        <PlayerPercentiles playerRapportRanking={playerRapport} />
        
        <ShotChart
          playerId={playerId}
          shotData={shotData}
        />
      </div>
    );
};

export default Dashboard;