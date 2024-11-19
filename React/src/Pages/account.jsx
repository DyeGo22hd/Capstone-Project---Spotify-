import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import OAuthLogin from '../Components/appwrite-oauth/appwrite-spotify.jsx';
import UserInfo from '../Components/appwrite-oauth/appwrite-session-info.jsx';

import { SessionContext } from '../App.jsx';

const Account = () => {
    const sessionInfo = useContext(SessionContext);
    const navigate = useNavigate();

    const handleLoginSuccess = (currentSession) => {
        sessionInfo.setSession(currentSession); // Save session info
        navigate('/success'); // Redirect to success route
    };

    return (
        <>
            {!sessionInfo.session && <h3>Not Logged In!</h3>}
            {!sessionInfo.session && <OAuthLogin onLoginSuccess={handleLoginSuccess} />}
            {sessionInfo.session && <h3>Logged In!</h3>}
            {sessionInfo.session && <UserInfo />}
        </>
    );
};

export default Account