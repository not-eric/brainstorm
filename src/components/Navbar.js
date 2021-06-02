import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const [click, setClick] = useState(false);
  const handleClick = () => setClick(!click);
  const exitMenu = () => setClick(false);

  return (
    <>
      <nav className="navbar">
        <div className="container">
          <NavLink to="/" className="logo">
            <img
              className="brainImage"
              src="/images/logo.png"
              alt="Electricity"
            ></img>
            BrainStorm
          </NavLink>
          <ul className={click ? "menu active" : "menu"}>
            <li>
              <NavLink to="/" className="links" onClick={exitMenu}>
                Home
              </NavLink>
            </li>
            <li>
              <NavLink to="/generator" className="links" onClick={exitMenu}>
                Generator
              </NavLink>
            </li>
            <li>
              <NavLink to="/about" className="links" onClick={exitMenu}>
                About
              </NavLink>
            </li>
          </ul>
          <div className="hamburger" onClick={handleClick}>
            <i className={click ? "fas fa-times" : "fas fa-bars"} />
          </div>
        </div>
      </nav>
    </>
  );
}

export default Navbar;
