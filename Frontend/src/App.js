import React from 'react';
import QueryForm from './components/QueryForm';
import Settings from './components/Settings';
import './App.css'; // You can remove this if not needed

function App() {
  return (
    <div className="App">
      <h1>NEXIS</h1>
      <QueryForm />
      <Settings />
    </div>
  );
}

export default App;
