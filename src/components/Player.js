import { Component } from 'react';
import { Midi } from '@tonejs/midi';
import * as Tone from 'tone';

export default class Player extends Component {
    constructor(props) {
        super(props);
        
        this.state = {
            filename: props.filename,
            mid: null,
            buttonText: "Play",
            disabled: false,
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
            });
            this.loadMidi();
        }
        if(this.state.disabled !== prevState.disabled) {

        }
    }

    loadMidi = async() => {
        let filename = this.props.filename;
        console.log("Getting file " + filename);
        
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

        let { mid, filename } = this.state;
        
        console.log(`Playing ${filename} now!\n`);
        
        console.log(mid);

        this.setState( {disabled: true} );
        setInterval(() => { 
            this.setState( {disabled: false}) 
        }, mid.duration * 1000);

        let playing = e.detail;
        
        let synths = [];

        if (playing && mid) {
            const now = Tone.now() + 0.5;
            mid.tracks.forEach((track) => {
                //create a synth for each track
                const synth = new Tone.PolySynth(Tone.Synth, {
                    envelope: {
                        attack: 0.02,
                        decay: 0.1,
                        sustain: 0.3,
                        release: 1,
                    },
                }).toDestination();
                synths.push(synth);
                //schedule all of the events
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
            //dispose the synth and make a new one
            while (synths.length) {
                const synth = synths.shift();
                synth.disconnect();
            }
        }

        
    }

    render() {
        
        return (
            <div className="player">
                <button 
                onClick={this.play} 
                disabled={this.state.disabled}>
                    {this.state.buttonText}
                </button>
                <p>{this.props.filename}</p>
            </div>
        );
    }

}