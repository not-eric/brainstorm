import { Component } from 'react';
import { Midi } from '@tonejs/midi';
import * as Tone from 'tone';
import "./Player.css";

export default class Player extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            filename: props.filename,
            mid: null,
            buttonText: "Play",
            disabled: false,
            songTitle: props.filename.substring(0, props.filename.indexOf(".mid")),
        };

        this.play = this.play.bind(this);
    }

    componentDidMount() {
        this.loadMidi();

        // Make sure audio context starts (must be after user interaction)
        document.getElementById('play')?.addEventListener('click', async () => {
            await Tone.start();
        })
    }

    componentDidUpdate(prevProps, prevState) {
        if(this.props.filename !== prevProps.filename) {
            this.setState({ 
                filename: this.props.filename,
                songTitle: this.props.filename.substring(0, this.props.filename.indexOf(".mid"))
            });
            this.loadMidi();
        }
        if(this.state.disabled !== prevState.disabled) {

        }
    }

    loadMidi = async() => {
        let filename = this.props.filename;
        // console.log("Getting file " + filename);
        
        await Midi.fromUrl(`http://localhost:5000/midi/${filename}`)
            .then((response) => 
            { 
                console.log("Successfully received file.");
                this.setState(
                {
                    mid: response,
                })
            });
        
    } 

    play(e) {
        e.preventDefault();

        let { mid } = this.state;
        
        // console.log(`Playing ${filename} now!\n`);
        // console.log(mid);

        this.setState( {disabled: true} );
        setInterval(() => { 
            this.setState( {disabled: false}) 
        }, mid.duration * 1000);

        let playing = e.detail;
        
        let synths = [];

        if (playing && mid) {
            const now = Tone.now() + 0.5;
            mid.tracks.forEach((track) => {
                // Create a synth for each MIDI track
                const synth = new Tone.PolySynth(Tone.Synth, {
                    envelope: {
                        attack: 0.02,
                        decay: 0.1,
                        sustain: 0.3,
                        release: 1,
                    },
                }).toDestination();
                synths.push(synth);
                // Schedule events for playback
                track.notes.forEach((note) => {
                    synth.triggerAttackRelease(
                        note.name,
                        note.duration,
                        note.time + now,
                        note.velocity
                    );
                });
            });

        } else {
            // Delete synth, create new ones
            while (synths.length) {
                const synth = synths.shift();
                synth.disconnect();
            }
        }

        
    }

    render() {
        
        return (
            <div className="player">
                <h1>{this.state.songTitle}</h1>
                <button 
                onClick={this.play} 
                disabled={this.state.disabled}>
                    {this.state.buttonText}
                </button>
            </div>
        );
    }

}