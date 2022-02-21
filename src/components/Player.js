import { Component } from 'react';
import { Midi } from '@tonejs/midi';
import * as Tone from 'tone';
import "./Player.css";
import abcjs from 'abcjs';

const host = process.env.REACT_APP_HOST_URL || 'http://localhost:5000'

/*
    Player component, renders underneath the form. Receives user data,
    and makes outbound requests depending on user choices.
*/
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
        // Updates the state as inputs are changed by the user
        this.setState({ 
            [event.target.name]: event.target.value,
        });
    }

    loadMidi = async() => {
        let filename = this.props.filename;
        
        // Asynchronously fetch the generated MIDI from the server
        await Midi.fromUrl(`${host}/midi/${filename}`)
            .then((response) => 
            { 
                console.log("Successfully received file.");

                // Update the state with the received and parsed MIDI data
                this.setState(
                {
                    mid: response,
                })

                // Renders the received notation as sheet music on the page,
                // and the options ensure the music is resized properly
                abcjs.renderAbc("paper", 
                    this.props.sheetmusic, 
                    { 
                        staffwidth: 500,
                        responsive: "resize" 
                    }
                );
            });
        
    } 

    play(e) {
        // Prevent clicking the buttons from refreshing the form
        e.preventDefault();

        let { mid } = this.state;
        
        // Reset the play button text approximately after the song finishes
        var timeout = setTimeout(() => { 
            this.setState( 
                {buttonText: "Play"}
            );
        }, 
            mid.duration * 1200
        );

        let playing = this.state.playing;
        
        let options = {
            'synth': Tone.Synth, 
            'am': Tone.AMSynth, 
            'duo': Tone.DuoSynth, 
            'mem': Tone.MembraneSynth, 
            'mono': Tone.MonoSynth, 
        }

        // If synths are in the state (if playback has started), load them
        let synths = [...this.state.synthz];

        if (!playing && mid) {

            this.setState({playing: true, buttonText: "Stop"});
            const now = Tone.now() + 0.5;

            mid.tracks.forEach((track) => {
                // Create a synth for each MIDI track
                var synth = new Tone.PolySynth(options[this.state.synth], {
                    envelope: {
                        attack: 0.02,
                        decay: 0.1,
                        sustain: 0.3,
                        release: 1,
                    },
                }).toDestination();

                // These are really loud by default
                if(this.state.synth === 'duo' 
                || this.state.synth === 'mem'
                || this.state.synth === 'synth') {
                    synth.volume.value = -12;
                }

                // And this one is really quiet by default
                if(this.state.synth === 'am') {
                    synth.volume.value = 2;
                }

                // Due to the structure of the function, both piano and strings have to
                // use the same structure except for the two varying fields.
                // Both load sound samples from external resources, and modulate accordingly.
                var option = this.state.synth;
                if(this.state.synth === 'piano' || this.state.synth === 'strings') {
                    if(option === 'piano') {
                        synth= new Tone.Sampler({
                            urls: {
                                A1: "A1.mp3",
                                A2: "A2.mp3",
                                A3: "A3.mp3",
                                A4: "A4.mp3",
                                A5: "A5.mp3",
                                A6: "A6.mp3"
                            },
                            baseUrl: "https://tonejs.github.io/audio/salamander/",
                            onload: () => {
                                synths.push(synth);
                                track.notes.forEach((note) => {
                                    synth.triggerAttackRelease(
                                        note.name,
                                        note.duration,
                                        note.time + now,
                                        note.velocity
                                    );
                                });
                
                                this.setState(
                                    {synthz: [...synths]}
                                );
                            }
                        }).toDestination();
                    } else {
                        synth= new Tone.Sampler({
                            urls: {
                                A3: "A3.mp3",
                                A4: "A4.mp3",
                                A5: "A5.mp3",
                                A6: "A6.mp3"
                            },
                            baseUrl: "https://nbrosowsky.github.io/tonejs-instruments/samples/violin/",
                            onload: () => {
                                synths.push(synth);
                                track.notes.forEach((note) => {
                                    synth.triggerAttackRelease(
                                        note.name,
                                        note.duration,
                                        note.time + now,
                                        note.velocity
                                    );
                                });
                
                                this.setState(
                                    {synthz: [...synths]}
                                );
                            }
                        }).toDestination();
                    }
                }
                else {
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

                    this.setState(
                        {synthz: [...synths]}
                    );
                }
            });

        } else {
            // If the button is clicked when the song is playing, clear timer and synths
            this.setState({playing: false, buttonText: "Play"});
            clearTimeout(timeout);

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
                <h1>Title: {this.state.songTitle}</h1>
                <button 
                    onClick={this.state.disabled ? null : this.play} 
                    disabled={this.state.disabled}>
                        {this.state.buttonText}
                </button>

                <a href={`${host}/midi/${this.state.filename}`} download>
                    Download
                </a>

                <div className="synthChoice">
                    <select name="synth" onChange={this.onChange}>
                        <option value="synth">Default Synth</option>
                        <option value="am">AMSynth</option>
                        <option value="duo">DuoSynth</option>
                        <option value="mem">MembraneSynth</option>
                        <option value="mono">MonoSynth</option>
                        <option value="piano">Piano</option>
                        <option value="strings">Strings</option>
                    </select>
                </div>
                <div id="paper"></div>
            </div>
        );
    }

}