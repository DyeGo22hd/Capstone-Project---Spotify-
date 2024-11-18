import PropTypes from 'prop-types';
import { useState, useEffect, useContext, useRef } from 'react';
import { PlaybackContext } from '../../Pages/spotify-player.jsx'

import TrackHTML from './track-display/track-container.jsx';
import TracksList from './track-display/tracks-list.jsx';

const Playback = ({ authToken }) => {
    const playerData = useContext(PlaybackContext);

    const [isLoadingPlayback, setLoadingPlayback] = useState(true);
    const [playbackData, setPlaybackData] = useState(undefined);
    const isFetching = useRef(false);

    const playbackLink = 'https://api.spotify.com/v1/me/player';
    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

	// real-time update from: https://stackoverflow.com/questions/39426083/update-react-component-every-second
    useEffect(() => {
        getCurrentPlayback();
        const interval = setInterval(getCurrentPlayback, 1000);
		return () => {
			clearInterval(interval);
		};
	}, []);

    const getCurrentPlayback = async () => {
        try {
            const response = await fetch(playbackLink, {
                method: "GET",
                headers: authHeader,
            });

            setLoadingPlayback(false);

            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const json = await response.json();
            setPlaybackData(json['item']);
        } catch (error) {
            console.log('API error: ', error);
        }
    };

    /*
    if (!isLoadingPlayback) {
        if (playbackData) {
            if (playbackData.id != playerData.currentSong) {
                playerData.setCurrentSong(playbackData.id);
            }
        }
        else if (playerData.currentSong) {
            playerData.setCurrentSong(null);
        }
    }
    */

    var playbackHTML = (
        <div>
            Playback Data Loading!
        </div>
    )

    if (!isLoadingPlayback) {
        if (!playbackData) {
            playbackHTML = (
                <div>
                    Not Playing Anything!
                </div>
            )
        }
        else {
            let currentData = (
                <TracksList>
                    <TrackHTML artists={playbackData.artists} name={playbackData.name} when={new Date()} length={playbackData.duration_ms} />
                </TracksList>
            );

            playbackHTML = (
                <div>
                    {currentData}
                </div>
            )
        }
    }

    return playbackHTML;
};

Playback.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default Playback;