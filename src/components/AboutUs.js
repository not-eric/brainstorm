import React from "react";
import "../App.css";
import "./AboutUs.css";
function AboutUs() {
  return (
    <div className="about-container">
      <div className="top">
        <h1 className="about">.about</h1>
        <p className="appDez">
          BrainStorm is a web application to help users in the creative process
          by <br></br>providing pseudo-randomly generated melodic ideas. This is
          achieved by utilizing <br></br>Python's built-in random() module in
          conjunction with a variety of mapping techniques <br></br> to make
          "decisions" about how to generate melodies based off several <br></br>
          different kinds of inputs. For this project, we used Python for the
          back-end and <br></br>
          CSS, Javascript, React for the front-end. We hope you enjoy your
          melody!
        </p>
        <h2 className="webDev">Web Developers:</h2>
      </div>
      <div className="bottom">
        <h3 className="jayName">Jay Derderian</h3>
        <div className="about-wrapper">
          <img
            className="jayFake"
            src="/images/einstein.jpeg"
            alt="synth cat in space"
          ></img>
          <img
            className="jayPic"
            src="/images/jared2.jpg"
            alt="just another cat"
          ></img>
        </div>
        <p className="jayDez">Back-end composer and fearless leader</p>
        <h3 className="jaredName">Jared Goldsmith</h3>
        <div className="about-wrapper">
          <img
            className="jaredFake"
            src="/images/einstein.jpeg"
            alt="synth cat in space"
          ></img>
          <img
            className="jaredPic"
            src="/images/jared2.jpg"
            alt="just another cat"
          ></img>
        </div>
        <p className="jaredDez">Front-end Reactionary and CSS laborer</p>
        <h3 className="ericName">Eric Dale</h3>
        <div className="about-wrapper">
          <img
            className="ericFake"
            src="/images/einstein.jpeg"
            alt="synth cat in space"
          ></img>
          <img
            className="ericPic"
            src="/images/jared2.jpg"
            alt="just another cat"
          ></img>
        </div>
        <p className="ericDez">
          The string to tie it all together, working <br></br>both the front-end
          and the back-end
        </p>
      </div>
      <div className="bottombottom">
        <p className="copyRight">&copy; BrainStorm</p>
      </div>
    </div>
  );
}

export default AboutUs;
