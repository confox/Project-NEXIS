import React, { useState } from 'react';
import axios from 'axios';

const QueryForm = () => {
  const [response, setResponse] = useState('');
  const [isRecording, setIsRecording] = useState(false);

  const startRecording = () => {
    setIsRecording(true);
  };

  const stopRecording = () => {
    setIsRecording(false);
    // Process and send the recorded audio to the backend
    sendAudioToBackend();
  };

  const sendAudioToBackend = async () => {
    try {
      // You need to implement this function to send audio data to the backend
      const audioData = {}; // Placeholder for audio data
      const res = await axios.post('/query', audioData);
      setResponse(res.data.response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Query Form</h2>
      {isRecording ? (
        <button onClick={stopRecording}>Stop Recording</button>
      ) : (
        <button onClick={startRecording}>Start Recording</button>
      )}
      {response && <p>Response: {response}</p>}
    </div>
  );
};

export default QueryForm;
