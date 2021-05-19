import React from "react";
import "../App.css";
import "./HomeDesign.css";

function HomeDesign() {
  return (
    <div className="home-container">
      <video
        className="homeVideo"
        src="/videos/video.mp4"
        autoPlay
        loop
        muted
      />
      <img
        className="catspace"
        src="/images/catsinspace.jpg"
        alt="synth cat in space"
      ></img>
      <h1>.home</h1>
    </div>
  );
}

export default HomeDesign;
