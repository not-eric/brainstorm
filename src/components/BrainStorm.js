import React from "react";
import "../App.css";
import "./BrainStorm.css";
/*import "./HomeDesign.css";*/
import Form from "./Form.js";

function BrainStorm() {
  return (
    <div className="gen-container">
      <h1 className="genTop"> .generator </h1>
      {/*<img className="modSynth" src="/images/photo2.png" alt="synthesizer" />*/}
      <img className="modSynth" src="/images/synth.png" alt="synthesizer" />
      <br></br>
      <Form />
    </div>
  );
}
export default BrainStorm;
