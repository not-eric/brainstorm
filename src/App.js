import React from "react";
import Navbar from "./components/Navbar";
import "./App.css";
import Home from "./components/webPages/Home";
import Generator from "./components/webPages/Generator";
import About from "./components/webPages/About";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/generator" exact component={Generator} />
          <Route path="/about" exact component={About} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
