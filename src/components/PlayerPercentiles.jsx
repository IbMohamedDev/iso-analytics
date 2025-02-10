import React from 'react';

export const PlayerPercentiles = ({ playerRapportRanking }) => {
  const player = playerRapportRanking || {
    name: "No Data Available",
    Off: 0,
    Def: 0,
    Tot: 0,
    WAR: 0,
    WAR82: 0
  };


  const percentiles = [
    { key: 'Offense', label: 'Offense', value: Math.round((player.Off + 6) * 10) }, 
    { key: 'Defense', label: 'Defense', value: Math.round((player.Def + 3) * 15) }, 
    { key: 'Overall', label: 'Overall', value: Math.round((player.Tot + 7) * 8) },  
    // { key: 'WAR', label: 'WAR', value: Math.round((player.WAR / 3.5) * 100) },     
    // { key: 'WAR82', label: 'WAR/82', value: Math.round((player.WAR82 / 17) * 100)} 
  ];

  return (
    <div className="mt-20 w-100">
    {<h1 className='text-center p-2 mb-5'>2024-25 Regular Season</h1>}
      <div className="space-y-2">
        {percentiles.map(({ key, label, value }) => (
          <div key={key} className="flex items-center gap-4">
            <div className="w-24 text-sm text-gray-600">{label}</div>
            <div className="flex-1">
              <div className="h-6 bg-gray-100 relative">
                <div
                  className="h-full bg-emerald-400"
                  style={{
                    width: `${Math.min(Math.max(value, 0), 100)}%`,
                    transition: 'width 0.5s ease-out'
                  }}
                />
              </div>
            </div>
            <div className="w-12 text-sm text-gray-600 text-right">
              {Math.min(Math.max(value, 0), 100)}
            </div>
          </div>
        ))}
      </div>
      
      {/* X-axis labels */}
      <div className="flex justify-between mt-2 px-24">
        <div className="text-sm text-gray-500">0</div>
        <div className="text-sm text-gray-500">50</div>
        <div className="text-sm text-gray-500">100</div>
      </div>
      <div className="text-center mt-4 text-gray-600">Percentile Ranking</div>
    </div>
  );
};
