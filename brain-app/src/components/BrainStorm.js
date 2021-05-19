import React from "react";
import "../App.css";
import "./BrainStorm.css";
import "./HomeDesign.css";

function BrainStorm() {
  return (
    <body>
      <div className="gen-container">
        <h2> .generator </h2>
        <img className="modSynth" src="/images/photo2.jpg" alt="synthesizer" />
        <br></br>
        <label class="friends" for="name">
          Input Name Here{" "}
        </label>
        <br></br>
        <input
          class="genName"
          id="inputdefault"
          type="name"
          name="name"
          required="required"
        />
        <button type="submit" class="submission">
          Submit
        </button>
      </div>
    </body>
  );
}
export default BrainStorm;
