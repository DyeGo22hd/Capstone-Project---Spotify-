import { useState, createContext, useEffect } from 'react'
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import viteLogo from '/vite.svg'
import './App.css'

import { account } from './Components/appwrite-oauth/appwrite-config.js';
import UserInfo from './Components/appwrite-oauth/appwrite-session-info.jsx';

import GetPlayback from './Pages/spotify-player.jsx';
import Homepage from './Pages/homepage.jsx';
import Navbar from './Components/page-elements/navbar.jsx';

export const SessionContext = createContext(undefined);


function App() {
    const [session, setSession] = useState(null);
    const navigate = useNavigate(); // Use navigate to redirect

    useEffect(() => {
        const checkSession = async () => {
            try {
                const currentSession = await account.getSession('current');
                console.log('Current session:', currentSession);
                setSession(currentSession); // Save session info
            } catch (error) {
                console.log('No active session:', error);
            }
        };

        checkSession();
    }, []);

    const goToPlayback = () => {
        navigate('/playback');
    };

    return (
        <div className="App">
            <Navbar />
            <Routes>
                <Route path="/playback" element={
                    <>
                        {session && <GetPlayback authToken={session.providerAccessToken}  />}
                    </>
                } />

                <Route path="/success" element={
                    <>
                        <div>Login Successful</div>
                        {session && <UserInfo/>} {/* Render UserInfo here */}
                        <button onClick={goToPlayback}>Go To PlayBack Data</button>
                    </>
                } />

                <Route path="/failed" element={<div>Login Failed</div>} />

                <Route path="/" element={
                    <>
                        <SessionContext.Provider value={{session, setSession}}>
                            <Homepage />
                        </SessionContext.Provider>
                        
                    </>
                } />                
            </Routes>
        </div>
    );
}

export default App
