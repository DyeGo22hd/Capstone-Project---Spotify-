import PropTypes from 'prop-types';
import { account } from './appwrite-config.js';

const OAuthLogOut = ({ onLogOutSuccess }) => {
    const handleLogOut = async () => {
        try {
            await account.deleteSession(
                'current'
            );
            onLogOutSuccess(); // Pass the session to App
        } catch (error) {
            console.error('Error during logout:', error);
        }
    };

    return (
        <button onClick={handleLogOut}>Log Out of Spotify</button>
    );
};

// PropTypes validation
OAuthLogOut.propTypes = {
    onLogOutSuccess: PropTypes.func.isRequired, // Ensure onLoginSuccess is a required function
};

export default OAuthLogOut;