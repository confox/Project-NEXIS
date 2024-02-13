const express = require('express');
const bodyParser = require('body-parser');
const speech = require('@google-cloud/speech');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(bodyParser.raw({ type: 'audio/wav', limit: '50mb' }));

let userPreferences = {
  theme: 'light',
  language: 'en',
};

app.post('/query', async (req, res) => {
  try {
    if (req.headers['content-type'] === 'application/json') {
      const { query } = req.body;
      const response = `Processing user query: ${query}`;
      res.json({ response });
    } else if (req.headers['content-type'] === 'audio/wav') {
      const audioData = req.body;
      fs.writeFileSync('audio.wav', audioData);
      const client = new speech.SpeechClient();
      const file = fs.readFileSync('audio.wav');
      const audioBytes = file.toString('base64');
      const audio = { content: audioBytes };
      const config = { encoding: 'LINEAR16', sampleRateHertz: 16000, languageCode: 'en-US' };
      const request = { audio: audio, config: config };
      const [response] = await client.recognize(request);
      const transcription = response.results.map(result => result.alternatives[0].transcript).join('\n');
      const responseText = `Processing user query: ${transcription}`;
      res.json({ response: responseText });
    }
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'An error occurred' });
  }
});

app.get('/settings', (req, res) => {
  res.json(userPreferences);
});

app.post('/settings', (req, res) => {
  const { theme, language } = req.body;
  userPreferences = { theme, language };
  res.json({ message: 'User preferences updated successfully' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
