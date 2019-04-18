import React from 'react';
import PrimaryAppBar from '../components/PrimaryAppBar';
import VirtualizedTable from '../components/VirtualizedTable';

export default class Home extends React.Component {
  render() {
    return (
      <div>
        <PrimaryAppBar />
        <VirtualizedTable />
      </div>
    );
  }
}
