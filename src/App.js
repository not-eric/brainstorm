import React from "react";
import Navbar from "./components/Navbar";
import "./App.css";
import Home from "./components/webPages/Home";
import Generator from "./components/webPages/Generator";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
  return (
    <>
      <Router>
        <Navbar />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/generator" exact component={Generator} />
        </Switch>
      </Router>
    </>
  );
}

export default App;
