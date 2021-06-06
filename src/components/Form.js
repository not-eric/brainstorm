import React, { Component } from 'react';
import axios from 'axios';
import Player from "./Player.js";
import "./Form.css";

export default class Form extends Component {
    constructor() {
        super();
        this.state = {
            name: '',
            res: '',
            planet: '',
            abc: '',
            dataReceived: false,
            key: 0,
            planet_lon: ''
        };
    }

    onChange = (event) => {
        this.setState({ 
            [event.target.name]: event.target.value,
        });
    }

    onSubmit = (event) => {
        event.preventDefault();       //prevent page refresh
        
        var { name } = this.state;     //pull from state

        // To avoid CORS errors, route request through custom router
        // in order to receive live planetary data
        axios.get('https://brain-cors.herokuapp.com/http://api.astrolin.org/now')
            .then((result) => {
                
                // The chosen planetary body's longitude is used for the input
                this.setState({
                    planet_lon: result.data.points[this.state.planet].lon
                })

                name += this.state.planet_lon;

                // POST request in here so that the longitude is received before POSTing
                axios.post('http://localhost:5000/api', { name })
                    .then((result) => {
                        let json = result.data;
                        this.setState( 
                            {
                                res: json.midititle, 
                                abc: json.sheetmusic,
                                dataReceived: true, 
                                key: Math.random()
                            } 
                        );
                    });
            }).catch(err => {
                // If there's an error, POST just the name field
                axios.post('http://localhost:5000/api', { name })
                    .then((result) => {
                        let json = result.data;
                        this.setState( 
                            {
                                res: json.midititle, 
                                abc: json.sheetmusic,
                                dataReceived: true, 
                                key: Math.random()
                            } 
                        );
                    });
            });
    }

    render() {
        const { name, res, dataReceived, abc} = this.state;

        return (
            <form onSubmit={this.onSubmit}>
                <input
                    type="text"
                    name="name"
                    value={name}
                    placeholder="Name"
                    onChange={this.onChange}
                />
                <select name="planet" onChange={this.onChange}>
                    <option value=""></option>
                    <option value="Mercury">Mercury</option>
                    <option value="Venus">Venus</option>
                    <option value="Mars">Mars</option>
                    <option value="Jupiter">Jupiter</option>
                    <option value="Saturn">Saturn</option>
                    <option value="Uranus">Uranus</option>
                    <option value="Neptune">Neptune</option>
                    <option value="Pluto">Pluto</option> {/* "but it's not a planet!" see next two */}
                    <option value="Sun">Sun</option>
                    <option value="Moon">Moon</option>
                </select>
                <button 
                    type="submit">
                        Submit
                </button>

                {dataReceived &&
                    <Player key={this.state.key} filename={res} sheetmusic={abc}/>
                }
                
            </form>
        );
    }
}