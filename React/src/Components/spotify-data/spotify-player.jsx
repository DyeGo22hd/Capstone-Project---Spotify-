import PropTypes from 'prop-types';
import { useState, useEffect } from 'react'

const GetPlayback = ({ authToken }) => {
    const [isLoadingHistory, setLoadingHistory] = useState(true);
    const [isLoadingQueue, setLoadingQueue] = useState(true);
    const [historyData, setHistoryData] = useState(undefined);
    const [queueData, setQueueData] = useState(undefined);

    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

    const recentlyPlayedLink = "https://api.spotify.com/v1/me/player/recently-played";
    const currentQueueLink = "https://api.spotify.com/v1/me/player/queue";

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
            setHistoryData(JSON.stringify(json['items']));

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
            setQueueData(JSON.stringify(json));
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
    var queueHTML = (
        <div>
            Queue Data Loading!
        </div>
    );

    if (!isLoadingHistory) {
        historyHTML = (
            <div>
                {historyData}
            </div>
        );
    };

    if (!isLoadingQueue) {
        queueHTML = (
            <div>
                {queueData}
            </div>
        );
    };

    return (
        <div>
            <button onClick={reload}>Reload Data</button>
            <h1>Recently Played Tracks</h1>
            {historyHTML}
            <h1>Current Queue</h1>
            {queueHTML}
        </div>
    );
};

GetPlayback.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default GetPlayback;