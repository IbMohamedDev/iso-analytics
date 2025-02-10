import React from 'react';

export const ShotChart = (props) => {
    
  
    const shots = Array.isArray(props.shotData) ? props.shotData : [props.shotData].filter(Boolean);

    const twoPointShots = shots.filter(shot => shot && shot.shotPts === 2);
    const threePointShots = shots.filter(shot => shot && shot.shotPts === 3);
    const twoPointMade = twoPointShots.filter(shot => shot && shot.madeShot).length;
    const threePointMade = threePointShots.filter(shot => shot && shot.madeShot).length;
    const twoPointPercentage = twoPointShots.length > 0 
      ? ((twoPointMade / twoPointShots.length) * 100).toFixed(1) 
      : '0.0';
    const threePointPercentage = threePointShots.length > 0 
      ? ((threePointMade / threePointShots.length) * 100).toFixed(1) 
      : '0.0';
      return (
        <>
          <div className="mt-10 w-150 max-w-3xl mx-auto p-2 flex flex-col items-center ">
            <h1 className="text-center mb-4">2024-25 Regular Season</h1>
            
            <svg viewBox="0 0 500 400" className="mt-2">
              <rect x="0" y="0" width="500" height="400" fill="none" stroke="black" strokeWidth="2" />
              <path d="M 0,300 A 240,240 0 0,1 500,300" fill="none" stroke="black" strokeWidth="2" />
              <circle cx="250" cy="300" r="60" fill="none" stroke="black" strokeWidth="2" />
              <rect x="170" y="300" width="160" height="100" fill="none" stroke="black" strokeWidth="2" />
              <line x1="220" y1="400" x2="280" y2="400" stroke="black" strokeWidth="4" />
              <circle cx="250" cy="400" r="7.5" fill="none" stroke="black" strokeWidth="2" />
      
              {shots.map((shot, index) => {
                if (!shot || typeof shot.x === 'undefined' || typeof shot.y === 'undefined') {
                  return null;
                }
      
                const flippedY = 400 - shot.y;
      
                const symbol = shot.shotPts === 2 ? (
                  <circle
                    cx={shot.x}
                    cy={flippedY}
                    r="5"
                    fill={shot.madeShot ? "#22c55e" : "#ef4444"}
                  />
                ) : (
                  <path
                    d={`M ${shot.x - 5},${flippedY - 5} L ${shot.x + 5},${flippedY + 5} M ${shot.x - 5},${flippedY + 5} L ${shot.x + 5},${flippedY - 5}`}
                    stroke={shot.madeShot ? "#22c55e" : "#ef4444"}
                    strokeWidth="2"
                  />
                );
                
                return <g key={index}>{symbol}</g>;
              })}
            </svg>
      
            <div className="mt-2 grid grid-cols-2 gap-2 text-center w-full max-w-sm">
              <div className="p-2 bg-gray-100 rounded">
                <h3 className="font-bold text-sm">2-Point Shots</h3>
                <p className="text-sm">{twoPointMade} / {twoPointShots.length} ({twoPointPercentage}%)</p>
              </div>
              <div className="p-2 bg-gray-100 rounded">
                <h3 className="font-bold text-sm">3-Point Shots</h3>
                <p className="text-sm">{threePointMade} / {threePointShots.length} ({threePointPercentage}%)</p>
              </div>
            </div>
          </div>
        </>
      );
      };
      
      export default ShotChart;