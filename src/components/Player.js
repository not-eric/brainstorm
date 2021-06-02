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
            synth: 'synth',
            playing: false,
            synthz: []
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

    componentWillUnmount() {
        // fixes "Warning: Can't perform a React state update on an unmounted component" error
        this.setState = (state, callback) => {
            return;
        };
    }

    onChange = (event) => {
        this.setState({ 
            [event.target.name]: event.target.value,
        });
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

       /*  this.setState( {disabled: true} );
        setTimeout(() => { 
            this.setState( {disabled: false});
        }, mid.duration * 1200); */

        let playing = this.state.playing;
        
        let options = {
            'synth': Tone.Synth, 
            'am': Tone.AMSynth, 
            'duo': Tone.DuoSynth, 
            'mem': Tone.MembraneSynth, 
            'mono': Tone.MonoSynth, 
            'pluck': Tone.PluckSynth
        }

        let synths = [...this.state.synthz];

        if (!playing && mid) {
            this.setState({playing: true, buttonText: "Stop"});
            const now = Tone.now() + 0.5;
            mid.tracks.forEach((track) => {
                // Create a synth for each MIDI track
                const synth = new Tone.PolySynth(options[this.state.synth], {
                    envelope: {
                        attack: 0.02,
                        decay: 0.1,
                        sustain: 0.3,
                        release: 1,
                    },
                }).toDestination();

                if(this.state.synth === 'duo') { // DuoSynth is REALLY LOUD
                    synth.volume.value = -12;
                }

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

                this.setState({synthz: [...synths]});
            });

        } else {
            this.setState({playing: false, buttonText: "Play"});
            
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
                onClick={this.state.disabled ? null : this.play} 
                disabled={this.state.disabled}>
                    {this.state.buttonText}
                </button>
                <div className="synthChoice">
                    <select name="synth" onChange={this.onChange}>
                        <option value="synth">Default Synth</option>
                        <option value="am">AMSynth</option>
                        <option value="duo">DuoSynth</option>
                        <option value="mem">MembraneSynth</option>
                        <option value="mono">MonoSynth</option>
                        <option value="pluck">PluckSynth</option>
                    </select>
                </div>
            </div>
        );
    }

}