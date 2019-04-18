import React, { Component } from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Home from './pages/Home';
import TestSensorData from './pages/TestSensorData';

class App extends Component {
  render() {
    return (
      <Router>
        <div>
          <Route path="/" exact component={
            Home
          } />
          <Route path="/test-sensor-data/" component={TestSensorData} />
        </div>
      </Router>
    );
  }
}

export default App;
