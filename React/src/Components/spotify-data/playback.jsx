import PropTypes from 'prop-types';
import { useState, useEffect, useContext } from 'react';
import { PlaybackContext } from '../../Pages/spotify-player.jsx'

import TrackHTML from './track-display/track-container.jsx';

const Playback = ({ authToken }) => {
    const currentSongRef = useContext(PlaybackContext);
    const [currentSongState, setCurrentSongState] = useState(currentSongRef.current);

    const [isLoadingPlayback, setLoadingPlayback] = useState(true);
    const [playbackData, setPlaybackData] = useState(undefined);

    const playbackLink = 'https://api.spotify.com/v1/me/player';
    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

	// real-time update from: https://stackoverflow.com/questions/39426083/update-react-component-every-second
    useEffect(() => {
        getCurrentPlayback();
        currentSongRef.current = currentSongState;
        const interval = setInterval(getCurrentPlayback, 30000);
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

            if (playbackData) {
                if (playbackData.id != currentSongState) {
                    setCurrentSongState(playbackData.id);
                }
            }
            else if (currentSongState) {
                setCurrentSongState(null);
            }
        } catch (error) {
            console.log('API error: ', error);
        }
    };

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
                <TrackHTML artists={playbackData.artists} name={playbackData.name} when={new Date()} length={playbackData.duration_ms} />
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