import { createContext, useEffect, useState, useContext } from 'react';
import { account } from '../Components/appwrite-oauth/appwrite-config.js';

const SessionContext = createContext(undefined);

const SessionProvider = ({ children }) => {
    const [session, setSession] = useState(undefined);

    useEffect(() => {
        const checkSession = async () => {
            try {
                const currentSession = await account.getSession('current');
                //console.log('Current session:', currentSession);
                setSession(currentSession); // Save session info
            } catch (error) {
                //console.log('No active session:', error);
                setSession(null);
            }
        };

        checkSession();
    }, []);

    return (
        <SessionContext.Provider value={{ session, setSession }} >
            { children }
        </ SessionContext.Provider >
    )
};

const UseSessionContext = () => {
    return useContext(SessionContext);
};

export { SessionProvider, UseSessionContext };