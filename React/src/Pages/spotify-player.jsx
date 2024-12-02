import PropTypes from 'prop-types';
import {useEffect, useState, createContext, useRef} from 'react';

import './spotify-player.css';

import Playback from '../Components/spotify-data/playback.jsx';
import Queue from '../Components/spotify-data/queue.jsx';
import History from '../Components/spotify-data/history.jsx';

export const PlaybackContext = createContext(undefined);

const GetCurrent = ({ authToken }) => {
    const currentSong = useRef(undefined);

    var currentHTML = (
        <>
            <h2>Currently Playing</h2>
            <PlaybackContext.Provider value={currentSong}>
                <Playback authToken={authToken}/>
            </PlaybackContext.Provider>
        </>
    );

    var historyHTML = (
        <>
            <div className='list-container'>
                <h2>Recently Played Tracks</h2>
                <PlaybackContext.Provider value={currentSong}>
                    <History authToken={authToken} />
                </PlaybackContext.Provider>
            </div>
        </>
    );

    var queueHTML = (
        <>
            <div className='list-container'>
                <h2>Current Queue</h2>
                <PlaybackContext.Provider value={currentSong}>
                    <Queue authToken={authToken} />
                </PlaybackContext.Provider>
            </div>
        </>
    );

    return (
        <>
            <div className='curent-player'>
                {currentHTML}
                <hr style={{ width: '90%' }}></hr>
            </div>
            
            <div className='box'>
                {historyHTML}
                {queueHTML}
            </div>
        </>
    );
};

GetCurrent.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default GetCurrent;