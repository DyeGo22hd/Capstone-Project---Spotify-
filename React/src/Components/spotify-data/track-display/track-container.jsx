const TrackHTML = ({artists, name, when, length}) => {
    const formatDuration = (duration_ms) => {
        const totalSeconds = Math.floor(duration_ms / 1000); // Convert ms to seconds
        const minutes = Math.floor(totalSeconds / 60); // Calculate minutes
        const seconds = totalSeconds % 60; // Calculate remaining seconds

        // Format seconds to always have two digits
        const formattedSeconds = seconds.toString().padStart(2, '0');

        return `${minutes}:${formattedSeconds}`; // Construct final string
    };

    const formatTime = (played_at) => {
        // Convert the date-time string to a Date object
        const date = new Date(played_at);

        // Create a formatter for New York local time
        const options = {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true, // Use 12-hour clock
            timeZone: 'America/New_York' // Set the timezone to New York
        };

        const formatter = new Intl.DateTimeFormat('en-US', options);

        // Format the date to mm/dd/yyyy
        const formattedDate = formatter.format(date);

        return formattedDate;
    }

    const artistNames = artists.map(artist => artist.name).join(', ');
    const formattedLength = formatDuration(length);
    const formattedDate = formatTime(when);

    return(
        <div>
            <h4> Track </h4>
            <hr style={{width:'25%'}}></hr>
            <p> Artists: {artistNames} </p>
            <p> Name: {name} </p>
            <p> Length: {formattedLength} </p>
            <p> Played: {formattedDate} </p>
        </div>
    );
};

export default TrackHTML;