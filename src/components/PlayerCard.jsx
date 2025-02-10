import React, { useState, useEffect } from "react";


export const PlayerCard = ({ playerData }) => {
  const [player, setPlayer] = useState({});
  const [stats, setStats] = useState({});
  const [headShotUrl, setHeadShotUrl] = useState("");
  const [age, setAge] = useState(0);
  const [seasons, setSeasons] = useState(0);
  const [allNba, setAllNba] = useState(0);
  const [champ, setChamp] = useState(0);
  const [mvp, setMvp] = useState(0);
  const [allDef, setAllDef] = useState(0);

  useEffect(() => {
    if (!playerData) return;

    setPlayer(playerData.player || {});
    setStats(playerData.stats || {});
    setHeadShotUrl(playerData.headshot_url || "");

    // Calculate awards
    let defAward = 0, allNbaAward = 0, mvpAward = 0, champAward = 0;
    if (playerData.awards) {
      playerData.awards.forEach((award) => {
        if (award.award === "All-Defensive") defAward++;
        else if (award.award === "NBA Champion") champAward++;
        else if (award.award === "All-NBA") allNbaAward++;
        else if (award.award === "MVP") mvpAward++;
      });
    }

    setAllDef(defAward);
    setAllNba(allNbaAward);
    setChamp(champAward);
    setMvp(mvpAward);

    // Calculate age
    if (playerData.player?.birth_date) {
      const today = new Date();
      const birthDateObj = new Date(playerData.player.birth_date);
      let tempAge = today.getFullYear() - birthDateObj.getFullYear();
      if (
        today.getMonth() < birthDateObj.getMonth() ||
        (today.getMonth() === birthDateObj.getMonth() && today.getDate() < birthDateObj.getDate())
      ) {
        tempAge--;
      }
      setAge(tempAge);
    }

    // Calculate seasons
    if (playerData.player?.to && playerData.player?.from) {
      setSeasons(playerData.player.to - playerData.player.from);
    }
  }, [playerData]);

  if (!playerData) return <div>No player data available.</div>;

  return (
   

<div className="max-w-xs mx-auto mt-5 mb-4 bg-white border border-gray-300 rounded-lg shadow-lg p-4 ">
      {/* Player Image Section */}
      <div className="relative  rounded-lg">
      {/* <h1 className="text-center bold ">Luka Dončić</h1> */}
        <img
          className="w-full object-cover rounded-t-xl border border-gray-300 "
          src={headShotUrl}
          alt=""
        />
        {/* <span className="absolute top-2 left-2 bg-orange-500 text-white text-xs font-bold px-1.5 py-0.5 rounded-md">
          !
        </span> */}
      </div>

      {/* Position Label */}
      <div className="mt-1">
        {/* Updated grid layout for perfect alignment */}
        <div className="grid grid-cols-3 gap-1">
          <div className="flex flex-col">
            <span className="bg-black text-white text-xs text-center font-bold uppercase px-2 py-1 rounded">Name</span>
            <span className="text-md font-bold mt-1 text-center">{player.player}</span>
          </div>
          
          <div className="flex flex-col">
            <span className="bg-black text-white text-xs text-center font-bold uppercase px-2 py-1 rounded">Position</span>
            <span className="text-md font-bold mt-1 text-center">{player.position}</span>
          </div>
          
          <div className="flex flex-col">
            <span className="bg-black text-white text-xs text-center font-bold uppercase px-2 py-1 rounded">Team</span>
            <span className="text-black-400 text-md font-bold mt-1 text-center">{player.team}</span>
          </div>
        </div>
      
  
  
</div>

  

      {/* Player Details */}
      <div className="grid grid-cols-4 h-14 gap-2 text-sm font-semibold border-t border-b border-gray-400 py-2 mt-1">
        <div className="border-r  border-gray-400 p-1">
          HEIGHT <br />
          <span className="text-md font-bold">{player.height}"</span>
        </div>
        <div className="border-r border-gray-400 p-1">
          AGE <br />
          <span className="text-md font-bold">{age}</span>
        </div>
        <div className="border-r border-gray-400 p-1">
          WEIGHT <br />
          <span className="text-md font-bold">{player.weight}lbs</span>
        </div>
        <div className="p-1">
          SEASON <br />
          <span className="text-md font-bold">{seasons}</span>
        </div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-4 text-center mt-1 text-sm font-semibold border-b border-gray-400">
        <div>
          <p className="text-2xl font-bold">{stats.pts}</p>
          <p className="text-gray-500">PTS</p>
        </div>
        <div>
          <p className="text-2xl font-bold">{stats.ast}</p>
          <p className="text-gray-500">AST</p>
        </div>
        <div>
          <p className="text-2xl font-bold">{stats.trb}</p>
          <p className="text-gray-500">TRB</p>
        </div>
        <div>
          <p className="text-2xl font-bold">{stats.fg3_per}</p>
          <p className="text-gray-500">3P%</p>
        </div>
      </div>

      {/* Awards Section */}
      <div className="grid grid-cols-4 gap-2 text-xs text-gray-400 mt-4">
        <div className="flex flex-col items-center">
          <div className="h-20 flex items-center justify-center">
            <img 
              className={`w-10 ${champ === 0 ? "opacity-25" : "opacity-100"}`}
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Larry_O%27Brien_Championship_Trophy_icon.svg/196px-Larry_O%27Brien_Championship_Trophy_icon.svg.png"
              alt="Championship Trophy"
            />
          </div>
          <p className={`mt-1 text-center ${champ == 0 ? "text-gray-400 " : "text-black font-bold"}`}>{champ}
          x Champion</p>
        </div>

        <div className="flex flex-col items-center">
          <div className="h-20 flex items-center justify-center">
            <img 
              className={`w-10 ${mvp === 0 ? "opacity-25" : "opacity-100"}`}
              src="https://www.pngkey.com/png/full/175-1756849_nba-mvp-trophy-png.png"
              alt="MVP Trophy"
            />
          </div>
          <p className={`mt-1 text-center ${mvp == 0 ? "text-gray-400 " : "text-black font-bold"}`}>{mvp}x</p>
          <p className={`mt-1 text-center ${allNba == 0 ? "text-gray-400 " : "text-black font-bold"}`}>MVP</p>
        </div>

        <div className="flex flex-col items-center">
          <div className="h-20 flex items-center justify-center">
            <img 
              className={`w-10 ${allNba === 0 ? "opacity-25" : "opacity-100"}`}
              src="https://cdn.freebiesupply.com/images/large/2x/nba-logo-transparent.png"
              alt="NBA Logo"
            />
          </div>
          <p className={`mt-1 text-center ${allNba == 0 ? "text-gray-400 " : "text-black font-bold"}`}>
          {allNba}x </p>
          <p className={`mt-1 text-center ${allNba == 0 ? "text-gray-400 " : "text-black font-bold"}`}>All-NBA</p>
        </div>

        <div className="flex flex-col items-center">
          <div className="h-20 flex items-center justify-center">
            <img 
              className={`w-19 ${allDef === 0 ? "opacity-25" : "opacity-100"}`}
              src="https://image.spreadshirtmedia.com/image-server/v1/designs/1000280492,height=100.png"
              alt="All-Defensive Team"
            />
          </div>
          <p className={`mt-1 text-center ${allDef == 0 ? "text-gray-400 " : "text-black font-bold"}`}>{allDef}x All-Defensive</p>
        </div>
      </div>

      {/* Draft Info */}
      <div className="border-t border-gray-400 mt-2 pt-1 text-center text-sm font-semibold ">
        <p className="uppercase text-gray-600">Drafted</p>
        <p className="font-bold">No. {player.draft_number} overall, {player.draft_year}</p>
      </div>
    </div>
  );
};
