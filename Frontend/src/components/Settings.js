import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Settings = () => {
  const [theme, setTheme] = useState('');
  const [language, setLanguage] = useState('');

  useEffect(() => {
    // Fetch user preferences from backend when component mounts
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const res = await axios.get('/settings');
      setTheme(res.data.theme);
      setLanguage(res.data.language);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleThemeChange = (event) => {
    setTheme(event.target.value);
  };

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  const handleSaveSettings = async () => {
    try {
      await axios.post('/settings', { theme, language });
      alert('User preferences saved successfully');
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Settings</h2>
      <label>
        Theme:
        <input type="text" value={theme} onChange={handleThemeChange} />
      </label>
      <label>
        Language:
        <input type="text" value={language} onChange={handleLanguageChange} />
      </label>
      <button onClick={handleSaveSettings}>Save Settings</button>
    </div>
  );
};

export default Settings;
