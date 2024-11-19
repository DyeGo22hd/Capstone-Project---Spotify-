import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import OAuthLogin from '../Components/appwrite-oauth/appwrite-spotify.jsx';

import { SessionContext } from '../App.jsx';

const Homepage = () => {
    const sessionInfo = useContext(SessionContext);
    const navigate = useNavigate();

    const handleLoginSuccess = (currentSession) => {
        sessionInfo.setSession(currentSession); // Save session info
        navigate('/success'); // Redirect to success route
    };

    return (
        <>
            <OAuthLogin onLoginSuccess={handleLoginSuccess} />
        </>
    );
};

export default Homepage