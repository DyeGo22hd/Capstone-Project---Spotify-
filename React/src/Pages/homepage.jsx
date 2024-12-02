import { useContext } from 'react';

import GetPlayback from './spotify-player.jsx';

import { UseSessionContext } from '../logic-necessary/session-provider.jsx';

const Homepage = () => {
    const sessionInfo = UseSessionContext();

    return (
        <>
            {!sessionInfo.session && <p>Not Logged In!</p>}
            {sessionInfo.session && <GetPlayback authToken={sessionInfo.session.providerAccessToken} />}
        </>
    );
};

export default Homepage