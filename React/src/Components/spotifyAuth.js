
//PKCE flow for auth https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow

//client id from alvi's dashboard 
const CLIENT_ID = "b24b1c78e21f447f8c7dce1d2a9d06c5"
const SPOTIFY_AUTHORIZE_ENDPOINT = "https://accounts.spotify.com/authorize" //base url for authorization request 
const REDIRECT_URL_AFTER_LOGIN = "http://localhost:3000/callback" 
const RESPONSE_TYPE = 'code';
const SCOPES = ["user-top-read"];

//code verifier for PKCE 
const generateRandomString = (length) => {
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const values = crypto.getRandomValues(new Uint8Array(length));
    return values.reduce((acc, x) => acc + possible[x % possible.length], "");
  }
  
  const codeVerifier  = generateRandomString(64);

//code challege used to hash generated code verfier, will be used for auth request
export const generateCodeChallenge = async (codeVerifier) => {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(codeVerifier));
    return btoa(String.fromCharCode(...new Uint8Array(digest)))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
  };

//spotify auth function using pkce 
export const authenticateSpotify = async () => {
    const codeVerifier = generateRandomString(128);
    const codeChallenge = await generateCodeChallenge(codeVerifier);
    localStorage.setItem('code_verifier', codeVerifier);

    const authURL = `${SPOTIFY_AUTHORIZE_ENDPOINT}?client_id=${CLIENT_ID}&response_type=${RESPONSE_TYPE}&redirect_uri=${encodeURIComponent(REDIRECT_URL_AFTER_LOGIN)}&scope=${SCOPES.join('%20')}&code_challenge_method=S256&code_challenge=${codeChallenge}`;
    window.location.href = authURL;
};