import PropTypes from 'prop-types';
import { useState, useEffect } from 'react';
import TrackHTML from './track-display/track-container.jsx';
import TracksList from './track-display/tracks-list.jsx';

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

    if (!isLoadingHistory && historyData) {
        historyHTML = (
            <div>
                <TracksList>
                    {historyData.map((item) => (<TrackHTML key={item.track.id} artists={item.track.artists} name={item.track.name} when={item.played_at} length={item.track.duration_ms}/>))}
                </TracksList>
            </div>
        );
    }
    else {
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
            currentData = (
                <TracksList>
                    {queueData['currently_playing'].map((item) => (<TrackHTML key={item.id} artists={item.artists} name={item.name} when={new Date()} length={item.duration_ms}/>))}
                </TracksList>
            );
        };
        if (queueData['queue']){
            futureData = (
                <TracksList>
                    {queueData['queue'].map((item) => (<TrackHTML key={item.id} artists={item.artists} name={item.name} when={new Date()} length={item.duration_ms}/>))}
                </TracksList>
            );
        };

        queueHTML = (
            <div>
                <h2> Currently Playing </h2>
                    {currentData}
                <h2> Future Queue </h2>
                    {futureData}
            </div>
        );
    }
    else {
        queueHTML = (
            <div>
                Data Empty!
            </div>
        );
    }

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