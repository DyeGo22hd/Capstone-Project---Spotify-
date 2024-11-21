import PropTypes from 'prop-types';
import { useState, useEffect, useContext, useRef } from 'react';
import { PlaybackContext } from '../../Pages/spotify-player.jsx'

import TrackHTML from './track-display/track-container.jsx';
import TracksList from './track-display/tracks-list.jsx';

const Queue = ({ authToken }) => {
    const currentSongRef = useContext(PlaybackContext);
    const currentSongState = useState(currentSongRef.current);

    const [isLoadingQueue, setLoadingQueue] = useState(true);
    const [queueData, setQueueData] = useState(undefined);

    const currentQueueLink = "https://api.spotify.com/v1/me/player/queue";
    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

    useEffect(() => {
        getQueue();
    }, []);

    useEffect(() => {
        getQueue();
    }, [currentSongState]);

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
            //console.log(JSON.stringify(json));
        } catch (error) {
            console.log('API error: ', error);
        }
    };

    var queueHTML = (
        <div>
            Queue Data Loading!
        </div>
    );

    if (!isLoadingQueue && queueData) {
        var futureData = (<div>Not playing anything!</div>);

        if (queueData['queue'] && queueData['queue'].length > 0) {
            futureData = (
                <TracksList>
                    {queueData['queue'].map((item) => (<TrackHTML key={item.id} artists={item.artists} name={item.name} when={new Date()} length={item.duration_ms} />))}
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
        <>
            { queueHTML }
        </>
    );
};

Queue.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default Queue;