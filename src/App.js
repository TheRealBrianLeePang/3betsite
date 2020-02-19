import React from 'react';
import logo from './logo.svg';
import './App.css';

var date = new Date().getDate(); //Current Date
var month = new Date().getMonth() + 1; //Current Month
var year = new Date().getFullYear(); //Current Year
var hours = new Date().getHours(); //Current Hours
var min = new Date().getMinutes(); //Current Minutes
var sec = new Date().getSeconds(); //Current Seconds


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Hello, welcome to a project called "Kanye West For President", a site/model for predicting
          spreads on upcoming NBA games.  Today is {month}, {date}, {year}.
        </p>
        <p>
          Click <a href='http://data.nba.net/10s/prod/v1/today.json' download>here</a> to 
          download today's stats.
        </p>
        
      </header>
    </div>
  );
}


export default App;
