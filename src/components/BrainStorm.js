import React from "react";
import "../App.css";
import "./BrainStorm.css";
/*import "./HomeDesign.css";*/
import Form from "./Form.js";

function hide(e) {
  var infobox = document.getElementsByClassName("how-to")[0];

  // Append the close class in order to trigger animation
  infobox.classList.add("close");
}

function BrainStorm() {
  return (
    <div className="gen-container">
      <div className="how-to">
        <h2>How to Use</h2>
        <p>Simply enter your name, optionally choose your favorite local celestial
          body to use its live coordinates, and receive a unique tune created
          based on your input. Try listening with different instruments and see
          what you get!
        </p>
        <button onClick={hide}>Dismiss</button>
      </div>
      <h1 className="genTop"> .generator </h1>
      {/*<img className="modSynth" src="/images/photo2.png" alt="synthesizer" />*/}
      <img className="modSynth" src="/images/synth.png" alt="synthesizer" />
      <br></br>
      <Form />
    </div>
  );
}
export default BrainStorm;
