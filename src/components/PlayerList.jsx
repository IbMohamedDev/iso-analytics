import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import TableCell from './TableCell'; 
import nbaTeams from '../nbaTeams'

export const PlayerList = () => {
  const [players, setPlayers] = useState([]);
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const [nameFilter, setNameFilter] = useState('');
  const [teamFilter, setTeamFilter] = useState('');
  const [positionFilter, setPositionFilter] = useState('');
  const itemsPerPage = 20;
  //const [playerImages, setPlayerImages] = useState({});

  const apiUrl = import.meta.env.VITE_API_URL;


  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const url = new URL(`${apiUrl}/players`);
        const params = { name: nameFilter, team: teamFilter, position: positionFilter };
        url.search = new URLSearchParams(params).toString();

        const response = await fetch(url);
        const playersData = await response.json();

        const statsUrl = `${apiUrl}/season_stats`;
        const statsResponse = await fetch(statsUrl);
        const statsData = await statsResponse.json();

        const statsLookup = statsData.reduce((acc, stat) => {
          acc[stat.player_id] = stat;
          return acc;
        }, {});

        const statsMap = playersData.reduce((acc, player) => {
          acc[player.player_id] = statsLookup[player.player_id] || {};
          return acc;
        }, {});

        setPlayers(playersData);
        setStats(statsMap);
      } catch (error) {
        console.error('Failed to fetch:', error);
      }
      setLoading(false);
    };

    fetchData();
  }, [nameFilter, teamFilter, positionFilter]);


    const sortedPlayers = [...players].sort((a, b) => {
    const statsA = stats[a.player_id] || {};
    const statsB = stats[b.player_id] || {};
    return (statsB.pts || 0) - (statsA.pts || 0);
  });

  const startIndex = (currentPage - 1) * itemsPerPage;
  const totalItems = sortedPlayers.length;
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const selectedData = sortedPlayers.slice(startIndex, startIndex + itemsPerPage);


  

  // useEffect(() => {
  //   const fetchImages = async () => {
  //     try {
  //       const playerNames = selectedData.map(player => player.player);
  //       const url = new URL('${apiUrl}/players/imgs');
  //       const params = { players: playerNames };
  //       url.search = new URLSearchParams(params).toString();

  //       const response = await fetch(url);
  //       const imageData = await response.json();

  //       setPlayerImages(imageData);
  //     } catch (error) {
  //       console.error('Failed to fetch images:', error);
  //     }
  //   };

  //   if (selectedData.length) {
  //     fetchImages();
  //   }
  // }, [selectedData]);

  if (loading) return <div className="p-4">Loading...</div>;

  return (
    <div className="overflow-x-auto m-8 bg-white p-6 rounded-lg shadow-lg">
      <div className="mb-6 flex flex-wrap gap-6">
        <div className="flex items-center space-x-2">
          <label className="text-gray-700">Name Filter:</label>
          <input type="text" value={nameFilter} onChange={(e) => setNameFilter(e.target.value)} placeholder="Filter by name" className="border border-gray-300 rounded-md px-3 py-1" />
        </div>
        <div className="flex items-center space-x-2">
          <label className="text-gray-700">Team Filter:</label>
          <select value={teamFilter} onChange={(e) => setTeamFilter(e.target.value)} className="border border-gray-300 rounded-md px-3 py-1">
            <option value="">Select Team</option>
            {nbaTeams.map((team) => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>
        <div className="flex items-center space-x-2">
          <label className="text-gray-700">Position Filter:</label>
          <select value={positionFilter} onChange={(e) => setPositionFilter(e.target.value)} className="border border-gray-300 rounded-md px-3 py-1">
            <option value="">Select Position</option>
            <option value="G-F">G-F</option>
            <option value="G">G</option>
            <option value="F">F</option>
            <option value="C">C</option>
          </select>
        </div>
      </div>

      <table className="min-w-full border-collapse border border-gray-300">
        <thead>
          <tr className="border-t hover:bg-gray-100 bg-gray-200">
            <TableCell >Player  </TableCell>
            <TableCell >Position </TableCell>
            <TableCell >Team </TableCell>
            <TableCell >PTS  </TableCell>
            <TableCell>FG% </TableCell>
            <TableCell>eFG%  </TableCell>
            <TableCell>PER </TableCell>
            <TableCell >AST </TableCell>
          </tr>
        </thead>
        <tbody>
          {selectedData.map((player, index) => {
            const playerStats = stats[player.player_id] || {};
            //const playerImage = playerImages[player.player];
            return (
              <tr key={index} className="border-t hover:bg-gray-300">
                <TableCell>
                  <div className="flex items-center space-x-2">
                    {/* {playerImage && (
                      <img
                        src={playerImage}
                        alt={player.player}
                        className="w-10 h-10 rounded-full"
                      />
                    )} */}
                    <Link to={`/player/${player.player_id}`} className="link-styles">
                      {player.player}
                    </Link>
                  </div>
                </TableCell>
                <TableCell>{player.position}</TableCell>
                <TableCell>{player.team}</TableCell>
                <TableCell>{playerStats.pts}</TableCell>
                <TableCell>{playerStats.fg_per}</TableCell>
                <TableCell>{playerStats.efg_per}</TableCell>
                <TableCell>{playerStats.per}</TableCell>
                <TableCell>{playerStats.ast}</TableCell>
              </tr>
            );
          })}
        </tbody>
      </table>

      <div className="flex justify-between items-center mt-6">
        <span>Items per page: {itemsPerPage}</span>
        <span>{startIndex + 1} – {Math.min(startIndex + itemsPerPage, totalItems)} of {totalItems}</span>
        <div>
          <button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50" onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))} disabled={currentPage === 1}>Prev</button>
          <button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50" onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))} disabled={currentPage === totalPages}>Next</button>
        </div>
      </div>
    </div>
  );
};



export default PlayerList;