import { useState, createContext, useEffect } from 'react'
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { account } from './Components/appwrite-oauth/appwrite-config.js';
import OAuthLogin from './Components/appwrite-oauth/appwrite-spotify.jsx';
import UserInfo from './Components/appwrite-oauth/appwrite-session-info.jsx';
import GetPlayback from './Components/spotify-data/spotify-player.jsx';


function App() {
    const [session, setSession] = useState(null);
    const [accessToken, setAccessToken] = useState(null);
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

    const handleLoginSuccess = (currentSession) => {
        setSession(currentSession); // Save session info
        navigate('/success'); // Redirect to success route
    };

    const goToPlayback = () => {
        navigate('/playback');
    };

    return (
        <div className="App">
            <h1>Appwrite OAuth2 with React</h1>
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
                <Route path="/" element={<OAuthLogin onLoginSuccess={handleLoginSuccess} />} />                
            </Routes>
        </div>
    );
}

export default App
