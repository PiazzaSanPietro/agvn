import React, { useState } from 'react';
import MainScreen from './components/MainScreen';
import LoadingScreen from './components/LoadingScreen';
import GameScreen from './components/GameScreen';
import apiService from './services/apiService';
import './App.css';

function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [storyData, setStoryData] = useState(null);
  const [error, setError] = useState(null);

  const handleStartGame = async (providedApiKey) => {
    setApiKey(providedApiKey);
    setIsLoading(true);
    setError(null);

    try {
      // Set API key in service
      apiService.setApiKey(providedApiKey);

      // Generate initial script with index 1
      const scriptData = await apiService.generateScript(1);

      setStoryData(scriptData);
      setIsLoading(false);
      setGameStarted(true);
    } catch (error) {
      console.error('Failed to generate initial script:', error);
      setError(error.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      {gameStarted ? (
        <GameScreen storyData={storyData} apiKey={apiKey} />
      ) : isLoading ? (
        <LoadingScreen />
      ) : (
        <MainScreen onStartGame={handleStartGame} error={error} />
      )}
    </div>
  );
}

export default App;
