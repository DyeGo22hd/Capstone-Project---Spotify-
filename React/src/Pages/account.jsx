import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import OAuthLogin from '../Components/appwrite-oauth/appwrite-spotify.jsx';
import OAuthLogOut from '../Components/appwrite-oauth/appwrite-logout.jsx';
import UserInfo from '../Components/appwrite-oauth/appwrite-session-info.jsx';

import { UseSessionContext } from '../logic-necessary/session-provider.jsx';

const Account = () => {
    const sessionInfo = UseSessionContext();
    const navigate = useNavigate();

    const handleLoginSuccess = (currentSession) => {
        sessionInfo.setSession(currentSession); // Save session info
        navigate('/account'); // Redirect to success route
    };

    const handleLogOutSuccess = () => {
        sessionInfo.setSession(null); // Update session info
        navigate('/account'); // Redirect to account route
    };

    if (sessionInfo) {
        return (
            <>
                {!sessionInfo.session && <h3>Not Logged In!</h3>}
                {!sessionInfo.session && <OAuthLogin onLoginSuccess={handleLoginSuccess} />}
                {sessionInfo.session && <h3>Logged In!</h3>}
                {sessionInfo.session && <UserInfo />}
                {sessionInfo.session && <OAuthLogOut onLogOutSuccess={handleLogOutSuccess} />}
            </>
        );
    }
    else {
        return (
            <>
                <h3>Not Logged In!</h3>
                <OAuthLogin onLoginSuccess={handleLoginSuccess} />
            </>
        )
    }
    
};

export default Account