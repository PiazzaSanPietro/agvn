import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const LoadingContainer = styled.div`
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const BackgroundImage = styled.img`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
`;

const GradientOverlay = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0.1) 40%,
    rgba(0, 0, 0, 0.3) 70%,
    rgba(0, 0, 0, 0.6) 90%,
    rgba(0, 0, 0, 0.8) 100%
  );
  z-index: 1;
`;

const LoadingText = styled.div`
  position: absolute;
  bottom: 40px;
  right: 40px;
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  z-index: 2;
  font-family: 'Arial', sans-serif;
  
  @media (max-width: 768px) {
    bottom: 30px;
    right: 30px;
    font-size: 1.2rem;
  }
  
  @media (max-width: 480px) {
    bottom: 20px;
    right: 20px;
    font-size: 1rem;
  }
`;

const LoadingScreen = () => {
  const [dots, setDots] = useState(0);
  const [backgroundImage, setBackgroundImage] = useState('');

  // Initialize random background on component mount
  useEffect(() => {
    const backgrounds = ['castle.png', 'forest.png', 'village.png', 'dungeon.png'];
    const randomBackground = backgrounds[Math.floor(Math.random() * backgrounds.length)];
    setBackgroundImage(`/assets/backgrounds/${randomBackground}`);
  }, []);

  // Animate dots
  useEffect(() => {
    const interval = setInterval(() => {
      setDots(prevDots => (prevDots + 1) % 4);
    }, 500);

    return () => clearInterval(interval);
  }, []);

  // Generate loading text with animated dots
  const loadingTextWithDots = 'loading' + '.'.repeat(dots);

  return (
    <LoadingContainer>
      <BackgroundImage 
        src={backgroundImage} 
        alt="Loading background"
      />
      <GradientOverlay />
      <LoadingText>{loadingTextWithDots}</LoadingText>
    </LoadingContainer>
  );
};

export default LoadingScreen;