import PropTypes from 'prop-types';
import { useState, useEffect, createContext, useRef} from 'react';

import './spotify-player.css';

import TrackHTML from '../Components/spotify-data/track-display/track-container.jsx';
import TracksList from '../Components/spotify-data/track-display/tracks-list.jsx';
import Playback from '../Components/spotify-data/playback.jsx';
import Queue from '../Components/spotify-data/queue.jsx';

export const PlaybackContext = createContext(undefined);

const GetCurrent = ({ authToken }) => {
    const [isLoadingHistory, setLoadingHistory] = useState(true);
    const [historyData, setHistoryData] = useState(undefined);

    var currentSong = useRef(undefined);

    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

    const recentlyPlayedLink = "https://api.spotify.com/v1/me/player/recently-played";

    /*
    const historySearchParams = new URLSearchParams({
        limit: 50
    }).toString()
    */

    useEffect(() => {
        getHistory();
    })

    const getHistory = async () => {
        try {
            const response = await fetch(recentlyPlayedLink, {
                method: "GET",
                headers: authHeader,
            });

            setLoadingHistory(false);

            if (!response.ok) {
              throw new Error(`Response status: ${response.status}`);
            }

            const json = await response.json();
            setHistoryData(json['items']);

        } catch (error) {
            console.log('API error: ', error );
        }

       
    };

    const reload = async () => {
        try {
            setLoadingHistory(true);
            setLoadingQueue(true);
            setHistoryData(undefined);
            setQueueData(undefined);
            
            await getHistory();
            await getQueue();
        } catch (error) {
            console.log('Reload error:', error);
        }
    }

    var historyHTML = (
        <div>
            Playback History Loading!
        </div>
    );

    if (!isLoadingHistory && historyData) {
        historyHTML = (
            <div>
                <TracksList>
                    {historyData.map((item) => (<TrackHTML key={`${item.track.id}${item.played_at}`} artists={item.track.artists} name={item.track.name} when={item.played_at} length={item.track.duration_ms} />))}
                </TracksList>
            </div>
        );
    }
    else if (!isLoadingHistory) {
        historyHTML = (
            <div>
                Data Empty!
            </div>
        );
    };

    return (
        <div>
            <button onClick={reload}>Reload Data</button>
            <h2>Currently Playing</h2>
            <PlaybackContext.Provider value={currentSong}>
                <Playback authToken={authToken}/>
             </PlaybackContext.Provider>
            <hr></hr>
            <div className='box'>
                <div className='list-container'>
                    <h2>Recently Played Tracks</h2>
                    {historyHTML}
                </div>
                <div className='list-container'>
                    <h2>Current Queue</h2>
                    <PlaybackContext.Provider value={currentSong}>
                        <Queue authToken={authToken} />
                    </PlaybackContext.Provider>
                </div>
            </div>
        </div>
    );
};

GetCurrent.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default GetCurrent;