import { useState, createContext, useEffect } from 'react'
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from 'react-router-dom';
import viteLogo from '/vite.svg'
import './App.css'

import { account } from './Components/appwrite-oauth/appwrite-config.js';
import UserInfo from './Components/appwrite-oauth/appwrite-session-info.jsx';

import GetPlayback from './Pages/spotify-player.jsx';
import Homepage from './Pages/homepage.jsx';
import Account from './Pages/account.jsx';
import Navbar from './Components/page-elements/navbar.jsx';

export const SessionContext = createContext(undefined);


function App() {
    const [session, setSession] = useState(null);
    const navigate = useNavigate(); // Use navigate to redirect
    const location = useLocation();

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
        const initializeNavbar = () => {
            let currentPath = location.pathname;
            if (currentPath == '/') {
                currentPath = 'home';
            }
            else {
                currentPath = currentPath.substring(1);
            }
            Array.from(document.querySelector('ul#navbar').getElementsByTagName('a')).forEach(function (e) {
                e.classList.remove("active")
            });
            document.getElementById(currentPath).className = "active";
        };

        checkSession();
        initializeNavbar()
    }, []);

    const goToPlayback = () => {
        navigate('/playback');
    };

    return (
        <div className="App">
            <Navbar />
            <div className = "Page">
                <Routes>
                    <Route path="/playback" element={
                        <>
                            {session && <GetPlayback authToken={session.providerAccessToken}  />}
                        </>
                    } />

                    <Route path="/account" element={
                        <SessionContext.Provider value={{ session, setSession }}>
                            <Account />
                        </SessionContext.Provider>
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
        </div>
    );
}

export default App
