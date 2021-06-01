import React from "react";
import "../App.css";
import "./BrainStorm.css";
/*import "./HomeDesign.css";*/
import { DropdownMenu, MenuItem } from "react-bootstrap-dropdown-menu";
import Form from "./Form.js";

function BrainStorm() {
  return (
    <div className="gen-container">
      <video
        className="genVideo"
        src="/videos/video2.mp4"
        autoPlay
        loop
        muted
      />
      <h2> .generator </h2>
      <img className="modSynth" src="/images/photo2.jpg" alt="synthesizer" />
      <br></br>
      <Form />
    </div>
  );
}
export default BrainStorm;
