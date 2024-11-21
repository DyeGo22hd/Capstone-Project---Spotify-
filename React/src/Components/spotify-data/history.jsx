import PropTypes from 'prop-types';
import { useState, useEffect, useContext, useRef } from 'react';
import { PlaybackContext } from '../../Pages/spotify-player.jsx'

import TrackHTML from './track-display/track-container.jsx';
import TracksList from './track-display/tracks-list.jsx';

const History = ({ authToken }) => {
    const currentSongRef = useContext(PlaybackContext);
    const currentSongState = useState(currentSongRef.current);

    const [isLoadingHistory, setLoadingHistory] = useState(true);
    const [historyData, setHistoryData] = useState(undefined);

    const recentlyPlayedLink = "https://api.spotify.com/v1/me/player/recently-played";
    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

    useEffect(() => {
        getHistory();
    }, [currentSongState]);

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
            console.log('API error: ', error);
        }


    };

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
        <>
            {historyHTML}
        </>
    );
};

History.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default History;