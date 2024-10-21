import PropTypes from 'prop-types';
import { account, OAuthProvider } from './appwrite-config.js';

const OAuthLogin = ({ onLoginSuccess }) => {
    const handleLogin = async () => {
        try {
            await account.createOAuth2Session(
                OAuthProvider.Spotify, // Update with your OAuth provider
                'http://localhost:5173/success', // Redirect here on success
                'http://localhost:5173/failed', // Redirect here on failure
                ['user-read-email'] // Scopes
            );
            const currentSession = await account.getSession('current');
            onLoginSuccess(currentSession); // Pass the session to App
        } catch (error) {
            console.error('Error during login:', error);
        }
    };

    return (
        <button onClick={handleLogin}>Login with Spotify</button>
    );
};

// PropTypes validation
OAuthLogin.propTypes = {
    onLoginSuccess: PropTypes.func.isRequired, // Ensure onLoginSuccess is a required function
};

export default OAuthLogin;