import React from "react";
import ReactDOM from "react-dom";
import { fetchModule } from "vite";
import "./WebApp.css";

//example url after access token 
//https://example.com/callback#access_token=NwAExz...BV3O2Tk&token_type=Bearer&expires_in=3600&state=123
 
//client id from alvi's dashboard 
const CLIENT_ID = "b24b1c78e21f447f8c7dce1d2a9d06c5"
const SPOTIFY_AUTHORIZE_ENDPOINT = "https://accounts.spotify.com/authorize" //bae url for authorization request 
const REDIRECT_URL_AFTER_LOGIN = "http://localhost:3000" //add real one from alvi later 
const SPACE_DELIMITER = "%20";
const SCOPES = ["user-read-currently-playing"]; //different stuff from spotify https://developer.spotify.com/documentation/web-api/concepts/scopes#user-read-playback-position 
//playback scope doesn't work for accts that don't have premium "user-read-currently-playing"
const SCOPES_URL_PARAM = SCOPES.join(SPACE_DELIMITER);

//helper fx to get access token from local host url 
//maybe have something to handle the error state 
const getReturnedParamsFromSpotifyAuth = (hash) => {
    const stringAfterHashing = hash.substring(1);
    const paramsInURL = stringAfterHashing.split("&");
}

const WebApp = () => {
    window.location - '${SPOTIFY_AUTHORIZE_ENDPOINT}?client_id=${CLIENT_ID&redirect_url=${REDIRECT_URL_AFTER_LOGIN}&SCOPE=${SCOPES_URL_PARAM&response_type=token&show_dialog=true' //template literals 
    return (
        <div className="container">
            <h1> Login</h1>
            <button onClick={handleLogin}>Login to Spotify</button>
            <h2> Sign up </h2>
            <button onClick = {handleLogin}> Sign in with Spotify</button>
        </div>

        
    );
};

export default WebApp; 

//should have button that takes you to login to spotify page for your dashboard 
//after click agree it should take you back to WebApp 
//access token is in url 

