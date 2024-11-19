import PropTypes from 'prop-types';
import { useState, useEffect, createContext } from 'react';

import './spotify-player.css';

import TrackHTML from '../Components/spotify-data/track-display/track-container.jsx';
import TracksList from '../Components/spotify-data/track-display/tracks-list.jsx';
import Playback from '../Components/spotify-data/playback.jsx';

export const PlaybackContext = createContext(undefined);

const GetCurrent = ({ authToken }) => {
    const [isLoadingHistory, setLoadingHistory] = useState(true);
    const [isLoadingQueue, setLoadingQueue] = useState(true);
    const [historyData, setHistoryData] = useState(undefined);
    const [queueData, setQueueData] = useState(undefined);

    const [currentSong, setCurrentSong] = useState(undefined);

    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

    const recentlyPlayedLink = "https://api.spotify.com/v1/me/player/recently-played";
    const currentQueueLink = "https://api.spotify.com/v1/me/player/queue";

    /*
    const historySearchParams = new URLSearchParams({
        limit: 50
    }).toString()
    */

    useEffect(() => {
        getHistory();
        getQueue();
    }, [currentSong])

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

    const getQueue = async () => {
        try {
            const response = await fetch(currentQueueLink, {
                method: "GET",
                headers: authHeader,
            });

            setLoadingQueue(false);

            if (!response.ok) {
              throw new Error(`Response status: ${response.status}`);
            }

            const json = await response.json();
            setQueueData(json);
            if (queueData['currently_playing']) {
                const item = queueData['currently_playing'];
                setCurrentSong(item.id);
            }
            else {
                setCurrentSong(null);
            }
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
            setCurrentSong(undefined);
            
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
    var queueHTML = (
        <div>
            Queue Data Loading!
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

    if (!isLoadingQueue && queueData) {
        var currentData = (<div>Not playing anything!</div>);
        var futureData = (<div>Not playing anything!</div>);

        if (queueData['currently_playing']) {
            const item = queueData['currently_playing'];
            currentData = (
                <TracksList>
                    <TrackHTML artists={item.artists} name={item.name} when={new Date()} length={item.duration_ms}/>
                </TracksList>
            );
        };
        if (queueData['queue'] && queueData['queue'].length > 0) {
            futureData = (
                <TracksList>
                    {queueData['queue'].map((item) => (<TrackHTML key={item.id} artists={item.artists} name={item.name} when={new Date()} length={item.duration_ms}/>))}
                </TracksList>
            );
        };

        queueHTML = (
            <div>
                {futureData}
            </div>
        );
    }
    else if (!isLoadingQueue) {
        queueHTML = (
            <div>
                Data Empty!
            </div>
        );
    }

    return (
        <div>
            <button onClick={reload}>Reload Data</button>
            <h2>Currently Playing</h2>
            <PlaybackContext.Provider value={{currentSong, setCurrentSong}}>
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
                    {queueHTML}
                </div>
            </div>
        </div>
    );
};

GetCurrent.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default GetCurrent;