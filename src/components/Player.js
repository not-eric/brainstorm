const { Midi } = require('@tonejs/midi');


export default function Player(props) {
    const midi = new Midi(props.filename);
    return (
        <div className="player">
            <h1>{props.filename}</h1>
            <tone-play-toggle disabled></tone-play-toggle>
        </div>
    )
}