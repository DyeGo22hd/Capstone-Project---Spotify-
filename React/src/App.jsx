import { useState, createContext, useEffect } from 'react'
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation } from 'react-router-dom';
import viteLogo from '/vite.svg'
import './App.css'

import { account } from './Components/appwrite-oauth/appwrite-config.js';
import UserInfo from './Components/appwrite-oauth/appwrite-session-info.jsx';

import Homepage from './Pages/homepage.jsx';
import Account from './Pages/account.jsx';
import Navbar from './Components/page-elements/navbar.jsx';

import { SessionProvider } from './logic-necessary/session-provider.jsx';


function App() {
    const navigate = useNavigate(); // Use navigate to redirect
    const location = useLocation();

    useEffect(() => {
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

        initializeNavbar()
    }, []);

    const goToPlayback = () => {
        navigate('/playback');
    };

    return (
        <div className="App">
            <Navbar />
            <div className="Page">
                <SessionProvider>
                    <Routes>
                        <Route path="/account" element={
                            <Account />

                        } />

                        <Route path="/failed" element={<div>Login Failed</div>} />

                        <Route path="/" element={
                            <Homepage />
                        } />                
                    </Routes>
                </SessionProvider>
            </div>
        </div>
    );
}

export default App
