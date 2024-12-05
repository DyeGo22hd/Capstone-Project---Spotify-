import PropTypes from 'prop-types';
import { useState, useEffect, useContext } from 'react';
import { PlaybackContext } from '../../Pages/spotify-player.jsx'

import TrackHTML from './track-display/track-container.jsx';

const Playback = ({ authToken }) => {
    const currentSongRef = useContext(PlaybackContext);
    const [currentSongState, setCurrentSongState] = useState(currentSongRef.current);

    const [isLoadingPlayback, setLoadingPlayback] = useState(true);
    const [playbackData, setPlaybackData] = useState(undefined);
    const [playing, setPlaying] = useState(undefined);
    var progress;

    const playbackLink = 'https://api.spotify.com/v1/me/player';
    const authHeader = new Headers();
    authHeader.append("Authorization", `Bearer ${authToken}`);

	// real-time update from: https://stackoverflow.com/questions/39426083/update-react-component-every-second
    useEffect(() => {
        getCurrentPlayback();
        currentSongRef.current = currentSongState;

        const interval = setInterval(getCurrentPlayback, playbackData == null ? 1000 : playbackData.duration_ms - progress);
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

            progress = json.progress_ms;
            setPlaying(json.actions.disallows.resuming);

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
                <TrackHTML imageLink={playbackData['album']['images'][0]['url']} artists={playbackData.artists} name={playbackData.name} when={new Date()} length={playbackData.duration_ms} />
            );

            playbackHTML = (
                currentData
            )
        }
    }

    //----------------------------------------------------------------------------------------------


    const resumeLink = 'https://api.spotify.com/v1/me/player/play';
    const pauseLink = 'https://api.spotify.com/v1/me/player/pause';
    const skipLink = 'https://api.spotify.com/v1/me/player/next';
    const prevLink = 'https://api.spotify.com/v1/me/player/previous';

    const ResumeTrack = async () => {
        await fetch(resumeLink, {
            method: "PUT",
            headers: authHeader,
        });
    }
    const PauseTrack = async () => {
        await fetch(pauseLink, {
            method: "PUT",
            headers: authHeader,
        });
    }
    const NextTrack = async () => {
        await fetch(skipLink, {
            method: "POST",
            headers: authHeader,
        });
    }
    const PrevTrack = async () => {
        await fetch(prevLink, {
            method: "POST",
            headers: authHeader,
        });
    }

    var HTML_Play_Button = (
        <button onClick={ResumeTrack}>PLAY</button>
    )
    var HTML_Pause_Button = (
        <button onClick={PauseTrack}>PAUSE</button>
    )
    var HTML_Skip_Button = (
        <button onClick={NextTrack}>NEXT</button>
    )
    var HTML_Prev_Button = (
        <button onClick={PrevTrack}>PREV</button>
    )


    var playerHTML = <>playing not known</>;

    if (playing) {
        playerHTML = (
            <div className='player'>
                {HTML_Prev_Button}
                {HTML_Pause_Button}
                {HTML_Skip_Button}
            </div>
        )
    }
    else {
        playerHTML = (
            <div className='player'>
                {HTML_Prev_Button}
                {HTML_Play_Button}
                {HTML_Skip_Button}
            </div>
        )
    }


    return (
        <>
            { playbackHTML}
            { playerHTML }
        </>
    );
};

Playback.propTypes = {
    authToken: PropTypes.string.isRequired,
};

export default Playback;