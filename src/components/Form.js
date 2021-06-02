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
            dataReceived: false,
        };
    }

    onChange = (event) => {
        this.setState({ [event.target.name]: event.target.value });
    }

    onSubmit = (event) => {
        event.preventDefault();       //prevent page refresh
        
        const { name } = this.state;     //pull from state

        axios.post('http://localhost:5000/api', { name })
            .then((result) => {
                this.setState( {res: result.data} );
                this.setState( {dataReceived: true} );
            });
    }

    render() {
        const { name, res, dataReceived } = this.state;

        return (
            <form onSubmit={this.onSubmit}>
                <input
                    type="text"
                    name="name"
                    value={name}
                    placeholder="Name"
                    onChange={this.onChange}
                />
                <button 
                    type="submit">
                        Submit
                </button>

                {dataReceived &&
                    <Player filename={res}/>
                }
                
            </form>
        );
    }
}