import React from 'react'
import { Link } from 'react-router-dom';


export const NavBar = () => {
  return (
    <div className="border-b border-gray-200 bg-white">
      <div className="container mx-auto flex items-center px-6 py-4">
        {/* Left - Logo */}
        <div className="text-2xl font-bold mr-10">ISOanalytics</div>
        
        {/* Center - Navigation Links */}
        <nav className="hidden md:flex space-x-6 text-lg">
          <Link to="/players" className="text-gray-800 hover:text-gray-500">Players</Link>
          <Link to="/compare" className="text-gray-800 hover:text-gray-500">Compare</Link>
         
        </nav>

        {/* Right - Newsletter Signup */}
        <div className="flex items-center space-x-3 ml-auto">
      
         
        </div>
      </div>
    </div>
  );
};
  