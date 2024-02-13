const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;

app.use(bodyParser.json());

// Sample data for user preferences (replace with your own logic)
let userPreferences = {
  theme: 'light',
  language: 'en',
};

// Route handler for processing user queries
app.post('/query', (req, res) => {
  const { query } = req.body;

  // Process the user query (replace with your own logic)
  const response = `Processing user query: ${query}`;

  res.json({ response });
});

// Route handler for managing user preferences
app.get('/settings', (req, res) => {
  res.json(userPreferences);
});

app.post('/settings', (req, res) => {
  const { theme, language } = req.body;

  // Update user preferences (replace with your own logic)
  userPreferences = { theme, language };

  res.json({ message: 'User preferences updated successfully' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
