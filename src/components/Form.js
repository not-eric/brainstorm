import React, { Component } from 'react';
import axios from 'axios';
import Player from "./Player.js";
import "./Form.css";
import ephemeris from 'ephemeris';

const host = process.env.REACT_APP_HOST_URL || 'http://localhost:5000'

export default class Form extends Component {
    constructor() {
        super();
        this.state = {
            name: '',
            res: '',
            planet: 'mercury',
            abc: '',
            dataReceived: false,
            key: 0,
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

        var result = ephemeris.getAllPlanets(new Date(), -122.6784, 45.5152, 0);

        // The chosen planetary body's longitude is used for the input
        name += result.observed[this.state.planet].apparentLongitudeDd;

        axios.post(`${host}/api`, { name })
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
                    <option value="mercury">Mercury</option>
                    <option value="venus">Venus</option>
                    <option value="mars">Mars</option>
                    <option value="jupiter">Jupiter</option>
                    <option value="saturn">Saturn</option>
                    <option value="uranus">Uranus</option>
                    <option value="neptune">Neptune</option>
                    <option value="pluto">Pluto</option> {/* "but it's not a planet!" see next two */}
                    <option value="sun">Sun</option>
                    <option value="moon">Moon</option>
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