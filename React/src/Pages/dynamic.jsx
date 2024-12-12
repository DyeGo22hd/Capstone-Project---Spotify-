import React from "react";
import UploadAndGeneratePlaylist from "../components/backend/UploadAndGeneratePlaylist.jsx";
import { UseSessionContext } from "../logic-necessary/session-provider.jsx";

const Dynamic = () => {
    const sessionInfo = UseSessionContext();

    if (!sessionInfo.session || !sessionInfo.session.providerAccessToken) {
        return <p>You must be logged in to access this feature.</p>;
    }

    return (
        <div>
            <h1>Dynamic Playlist Generator</h1>
            <UploadAndGeneratePlaylist authToken={sessionInfo.session.providerAccessToken} />
        </div>
    );
};

export default Dynamic;
