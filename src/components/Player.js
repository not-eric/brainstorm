import { Component } from 'react';
import { Midi } from '@tonejs/midi';
import * as Tone from 'tone';



export default class Player extends Component {
    constructor(props) {
        super(props);
        this.state = {
            filename: props.filename,
            mid: null,
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

    loadMidi = async() => {
        const { filename } = this.state;
        console.log("Getting file");
        //    Midi.fromUrl(`http://localhost:3000/midi/${this.filename}`)
        await Midi.fromUrl(`http://localhost:5000/midi/${filename}`)
            .then((response) => 
            { 
                this.setState(
                {
                    mid: response,
                })
            });
    } 

    play(e) {
        const { mid, filename } = this.state;
        console.log(`Playing ${filename} now!\n`);
        e.preventDefault();
        
        let synths = [];
        let playing = e.detail;
        
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
                <button id="play" onClick={this.play}>Play</button>
                <p>Oh hi there!</p>
            </div>
        );
    }

}