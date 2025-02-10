import { useState } from 'react'
import '/src/App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { NavBar } from './components/NavBar'
import {PlayerCard} from './components/PlayerCard'
import PlayerList from './components/PlayerList';
import {ShotChart} from './components/ShotChart'
import Dashboard from './components/Dashboard'
import Compare from './components/Compare';

function App() {



  
  const [count, setCount] = useState(0)
 

  return (

    <>
   
   

   
   <BrowserRouter>
   <NavBar/>
      <Routes>
        <Route path="/players" element={<PlayerList />} />
        <Route path="/player/:playerId" element={<Dashboard/>}/>
        <Route path='/Compare' element={<Compare/>}/>
        <Route path='/' element={<PlayerList/>}/>
        <Route path='/player/' element={<PlayerList/>}/>
      
      </Routes>
    </BrowserRouter>
    </>
  )
}

export default App
