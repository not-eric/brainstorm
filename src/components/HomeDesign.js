import React from "react";
import "../App.css";
import "./HomeDesign.css";
import { Link } from "react-router-dom";

function HomeDesign() {
  return (
    <div className="home-container">
      <video
        className="homeVideo"
        src="/videos/video4.mp4"
        autoPlay
        loop
        muted
      />
      <img
        className="catspace"
        src="/images/catsinspace.jpg"
        alt="synth cat in space"
      ></img>
      <div className="topRight">
        <h2 className="headDes">
          &nbsp; BrainStorm Music Generation<br></br>
          {/*Generate a melody
        based off your name and other inputs. Can be used for to inspire your
        own projects, or merely a good time.*/}
        </h2>
        <div className="descriptions">
          <p className="description">Generate a melody based off your</p>
          <p className="description2">name and other inputs. Give it a spin</p>
          <p className="description3">and inspire your next project</p>
        </div>
        <h3 className="linkGen">
          <Link to="/generator" className="genlinks">
            goto.generator
          </Link>
        </h3>
      </div>
      <h1 className="homeSymbol">.home</h1>
    </div>
  );
}

export default HomeDesign;
