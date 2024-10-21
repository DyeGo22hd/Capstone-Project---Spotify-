import { account } from './appwrite-config.js';
import { useState, useEffect } from 'react'

const UserInfo = () => {
    const [session, setSession] = useState(null);

    useEffect(() => {
        const fetchSession = async () => {
            try {
                const currentSession = await account.getSession('current');
                setSession(currentSession);
            } catch (error) {
                console.error('Failed to get session:', error);
            }
        };

        fetchSession();
    }, []);

    if (!session) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <p>Provider: {session.provider}</p>
            <p>Provider UID: {session.providerUid}</p>
            <p>Access Token: {session.providerAccessToken}</p>
        </div>
    );
};

export default UserInfo;