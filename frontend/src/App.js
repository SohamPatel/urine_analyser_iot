import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import PrimaryAppBar from './components/PrimaryAppBar';
import VirtualizedTable from './components/VirtualizedTable';

class App extends Component {
  render() {
    return (
      <div>
        <PrimaryAppBar />
        <VirtualizedTable />
      </div>
    );
  }
}

export default App;
