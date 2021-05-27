import React from "react";
import "../App.css";
import "./BrainStorm.css";
/*import "./HomeDesign.css";*/
import { DropdownMenu, MenuItem } from "react-bootstrap-dropdown-menu";

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
      <form className="gen-form">
        <label
          text="Input Name Here"
          className="friends"
          htmlFor="name"
          place-content="center"
          text-align="center"
        >
          Input Name Here{" "}
        </label>
        <br></br>
        <input
          className="genName"
          id="inputdefault"
          type="name"
          name="name"
          required="required"
        />
        <br></br>
        <DropdownMenu iconColor="orange" className="dropdown">
          <MenuItem text="Happy" variant="success" id="dropdown-basic">
            Happy
          </MenuItem>
          <MenuItem text="Sad" variant="success" id="dropdown-basic">
            Sad
          </MenuItem>
        </DropdownMenu>
        <DropdownMenu iconColor="orange" className="dropdown">
          <MenuItem text="Red" variant="success" id="dropdown-basic">
            Red
          </MenuItem>
          <MenuItem text="Orange" variant="success" id="dropdown-basic">
            Orange
          </MenuItem>
          <MenuItem text="Yellow" variant="success" id="dropdown-basic">
            Yellow
          </MenuItem>
          <MenuItem text="Green" variant="success" id="dropdown-basic">
            Green
          </MenuItem>
          <MenuItem text="Blue" variant="success" id="dropdown-basic">
            Blue
          </MenuItem>
          <MenuItem text="Indigo" variant="success" id="dropdown-basic">
            Indigo
          </MenuItem>
          <MenuItem text="Violet" variant="success" id="dropdown-basic">
            Violet
          </MenuItem>
        </DropdownMenu>
        <DropdownMenu iconColor="orange" className="dropdown">
          <MenuItem text="Mercury" variant="success" id="dropdown-basic">
            Mercury
          </MenuItem>
          <MenuItem text="Venus" variant="success" id="dropdown-basic">
            Venus
          </MenuItem>
          <MenuItem text="Earth" variant="success" id="dropdown-basic">
            Earth
          </MenuItem>
          <MenuItem text="Mars" variant="success" id="dropdown-basic">
            Mars
          </MenuItem>
          <MenuItem text="Jupiter" variant="success" id="dropdown-basic">
            Jupiter
          </MenuItem>
          <MenuItem text="Saturn" variant="success" id="dropdown-basic">
            Saturn
          </MenuItem>
          <MenuItem text="Uranus" variant="success" id="dropdown-basic">
            Uranus
          </MenuItem>
          <MenuItem text="Neptune" variant="success" id="dropdown-basic">
            Neptune
          </MenuItem>
        </DropdownMenu>
        <DropdownMenu iconColor="orange" className="dropdown">
          <MenuItem text="Slow" variant="success" id="dropdown-basic">
            Slow
          </MenuItem>
          <MenuItem text="Fast" variant="success" id="dropdown-basic">
            Fast
          </MenuItem>
          <MenuItem text="In-Between" variant="success" id="dropdown-basic">
            In-Between
          </MenuItem>
        </DropdownMenu>
        <br></br>
        <button type="submit" className="submission" color="blue">
          Submit
        </button>
      </form>
    </div>
  );
}
export default BrainStorm;
