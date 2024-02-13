import React, { useState } from 'react';
import axios from 'axios';

const NexisApp = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');

  const handleQueryChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post('/query', { query });
      setResponse(res.data.response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h1>NEXIS</h1>
      <input
        type="text"
        value={query}
        onChange={handleQueryChange}
        placeholder="Enter your query"
      />
      <button onClick={handleSubmit}>Submit</button>
      {response && <p>{response}</p>}
    </div>
  );
};

export default NexisApp;
