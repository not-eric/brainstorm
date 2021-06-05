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
        };
    }

    onChange = (event) => {
        this.setState({ 
            [event.target.name]: event.target.value,
        });
    }

    onSubmit = (event) => {
        event.preventDefault();       //prevent page refresh
        
        let { name } = this.state;     //pull from state
        
        name += this.state.planet;

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
                {/* Warning label here for potentially offensive titles? */}
                {dataReceived &&
                    <Player key={this.state.key} filename={res} sheetmusic={abc}/>
                }
                
            </form>
        );
    }
}