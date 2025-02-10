import React, { useState, useEffect } from "react";
import { PlayerCard } from "./PlayerCard";


const apiUrl = import.meta.env.VITE_API_URL;

const fetchPlayers = async () => {
    
  try {
    const response = await fetch(`${apiUrl}/players`);
    if (!response.ok) throw new Error("Failed to fetch players");
    return await response.json();
  } catch (error) {
    console.error("Error fetching players:", error);
    return [];
  }
};

const fetchPlayerDetails = async (playerId) => {
  try {
    const response = await fetch(`${apiUrl}/player/${playerId}`);
    if (!response.ok) throw new Error("Failed to fetch player details");
    return await response.json();
  } catch (error) {
    console.error("Error fetching player details:", error);
    return null;
  }
};

const PlayerSearch = ({ players, onSelect, placeholder }) => {
  const [query, setQuery] = useState("");
  const filteredPlayers = players.filter((player) =>
    player.player.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="relative w-full">
      <input
        type="text"
        className="border p-2 rounded w-full"
        placeholder={placeholder}
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      {query && filteredPlayers.length > 0 && (
        <div className="absolute bg-white border mt-1 w-full max-h-40 overflow-y-auto shadow-lg z-10">
          {filteredPlayers.map((player) => (
            <div
              key={player.id}
              className="p-2 hover:bg-gray-200 cursor-pointer"
              onClick={async () => {
                const playerDetails = await fetchPlayerDetails(player.player_id);
                if (playerDetails) {
                  onSelect(playerDetails);
                }
                setQuery("");
              }}
            >
              {player.player}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default function Compare() {
  const [players, setPlayers] = useState([]);
  const [selectedPlayer1, setSelectedPlayer1] = useState(null);
  const [selectedPlayer2, setSelectedPlayer2] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadPlayers = async () => {
      try {
        const data = await fetchPlayers();
        setPlayers(data);
        if (data.length > 1) {
          // Fetch details for initial players
          const player1Details = await fetchPlayerDetails(data[0].player_id);
          const player2Details = await fetchPlayerDetails(data[1].player_id);
          setSelectedPlayer1(player1Details);
          setSelectedPlayer2(player2Details);
        }
      } catch (error) {
        console.error("Error loading initial data:", error);
      } finally {
        setLoading(false);
      }
    };
    loadPlayers();
  }, []);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  return (
    <div className="flex gap-4 p-4">
      <div className="w-1/2">
        <PlayerSearch 
          players={players} 
          onSelect={setSelectedPlayer1} 
          placeholder="Search Player 1" 
        />
        {selectedPlayer1 && <PlayerCard playerData={selectedPlayer1} />}
      </div>
      <div className="w-1/2">
        <PlayerSearch 
          players={players} 
          onSelect={setSelectedPlayer2} 
          placeholder="Search Player 2" 
        />
        {selectedPlayer2 && <PlayerCard playerData={selectedPlayer2} />}
      </div>
    </div>
  );
}