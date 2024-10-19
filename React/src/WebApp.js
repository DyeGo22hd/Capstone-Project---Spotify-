import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { authenticateSpotify } from './spotifyAuth';

function WebApp() {
  //state to store spotify acccess token
  const [token, setToken] = useState(null);

  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get('code');
    if (code) {
      getAccessToken(code);
    }
  }, []);
  
  //exhcange auth code for acess token
  const getAccessToken = async (code) => {
    const codeVerifier = localStorage.getItem('code_verifier');
    try {
      //POST request 
      const response = await axios.post('https://accounts.spotify.com/api/token', null, {
        params: {
          client_id: 'b24b1c78e21f447f8c7dce1d2a9d06c5',
          grant_type: 'authorization_code',
          code,
          redirect_uri: 'http://localhost:3000/callback',
          code_verifier: codeVerifier
        },
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      setToken(response.data.access_token);
      localStorage.setItem('spotify_token', response.data.access_token);
    } catch (error) {
      console.error('Error getting token', error);
    }
  };

  //spotify login when user clicks 
  const handleLogin = () => {
    authenticateSpotify();
  };

  return (
    <div className="WebApp">
      <header className="WebApp-header">
        {!token ? (
          <button onClick={handleLogin}>Login to Spotify</button>
        ) : (
          <div>
            <h1>Logged In</h1>
            <p>Your Spotify access token is: {token}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default WebApp;
