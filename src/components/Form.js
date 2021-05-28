import React, { Component } from 'react';
import axios from 'axios';

export default class Form extends Component {
    constructor() {
        super();
        this.state = {
            name: '',
        };
    }

    onChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
    }

    onSubmit = (event) => {
    event.preventDefault();       //prevent page refresh
    
    const { name } = this.state;     //pull from state
    console.log("Name is" + name);
    axios.post('http://localhost:5000/api', { name })
        .then((result) => {
        console.log(result);
        });
    }

    render() {
    const { name } = this.state;
    return (
        <form onSubmit={this.onSubmit}>
        <input
            type="text"
            name="name"
            value={name}
            onChange={this.onChange}
        />
        <button type="submit">Submit</button>
        </form>
        );
    }
}