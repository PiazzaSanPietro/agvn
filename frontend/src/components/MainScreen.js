import React, { useState } from 'react';
import styled from 'styled-components';

const MainContainer = styled.div`
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  font-family: 'Arial', sans-serif;
`;

const BackgroundOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, rgba(255, 215, 0, 0.1) 0%, rgba(0, 0, 0, 0.3) 70%);
  z-index: 0;
`;

const ContentContainer = styled.div`
  z-index: 1;
  text-align: center;
  max-width: 800px;
  padding: 40px;
`;

const GameTitle = styled.h1`
  font-size: 2.5rem;
  color: #ffd700;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.8);
  margin-bottom: 3rem;
  font-weight: bold;
  line-height: 1.3;
  letter-spacing: 2px;
  
  @media (max-width: 768px) {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  @media (max-width: 480px) {
    font-size: 1.5rem;
    letter-spacing: 1px;
  }
`;

const InputContainer = styled.div`
  margin-bottom: 2rem;
  width: 100%;
  max-width: 400px;
`;

const InputLabel = styled.label`
  display: block;
  color: #ffd700;
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  text-align: left;
`;

const ApiKeyInput = styled.input`
  width: 100%;
  padding: 12px 16px;
  font-size: 1rem;
  background: rgba(255, 215, 0, 0.1);
  border: 2px solid rgba(255, 215, 0, 0.3);
  border-radius: 10px;
  color: #ffffff;
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }
  
  &:focus {
    outline: none;
    border-color: rgba(255, 215, 0, 0.6);
    background: rgba(255, 215, 0, 0.15);
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.2);
  }
`;

const StartButton = styled.button`
  background: ${props => props.disabled 
    ? 'linear-gradient(145deg, rgba(128, 128, 128, 0.2) 0%, rgba(128, 128, 128, 0.1) 100%)'
    : 'linear-gradient(145deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 215, 0, 0.1) 100%);'
  };
  border: 2px solid ${props => props.disabled 
    ? 'rgba(128, 128, 128, 0.3)' 
    : 'rgba(255, 215, 0, 0.5);'
  };
  border-radius: 15px;
  color: ${props => props.disabled ? '#888888' : '#ffd700'};
  font-size: 1.5rem;
  font-weight: bold;
  padding: 15px 40px;
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  transition: all 0.3s ease;
  text-shadow: ${props => props.disabled 
    ? '2px 2px 4px rgba(0, 0, 0, 0.5)'
    : '2px 2px 4px rgba(0, 0, 0, 0.8);'
  };
  backdrop-filter: blur(5px);
  opacity: ${props => props.disabled ? '0.6' : '1'};
  
  &:hover {
    ${props => !props.disabled && `
      background: linear-gradient(145deg, rgba(255, 215, 0, 0.3) 0%, rgba(255, 215, 0, 0.2) 100%);
      border-color: rgba(255, 215, 0, 0.8);
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(255, 215, 0, 0.2);
    `}
  }
  
  &:active {
    ${props => !props.disabled && `
      transform: translateY(0);
      box-shadow: 0 4px 8px rgba(255, 215, 0, 0.1);
    `}
  }
  
  @media (max-width: 480px) {
    font-size: 1.2rem;
    padding: 12px 30px;
  }
`;

const ErrorMessage = styled.div`
  color: #ff6b6b;
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.3);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  text-align: left;
  backdrop-filter: blur(5px);
`;

const MainScreen = ({ onStartGame, error }) => {
  const [apiKey, setApiKey] = useState('dummy-api-key-for-testing');

  const handleStartGame = () => {
    onStartGame(apiKey);
  };

  return (
    <MainContainer>
      <BackgroundOverlay />
      <ContentContainer>
        <GameTitle>Ai Generated Love Comedy (Alpha)</GameTitle>
        {error && <ErrorMessage>{error}</ErrorMessage>}
        <InputContainer style={{ display: 'none' }}>
          <InputLabel htmlFor="apiKey">Google API Key</InputLabel>
          <ApiKeyInput
            id="apiKey"
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter your Google API key..."
          />
        </InputContainer>
        <StartButton
          onClick={handleStartGame}
          disabled={false}
        >
          start
        </StartButton>
      </ContentContainer>
    </MainContainer>
  );
};

export default MainScreen;