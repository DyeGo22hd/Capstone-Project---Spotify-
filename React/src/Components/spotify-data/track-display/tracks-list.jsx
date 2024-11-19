import './tracks-list.css';

const TracksList = (props) => {
	return (
		<div className="tracks-list">
			{props.children}
		</div>
	);
};

export default TracksList;