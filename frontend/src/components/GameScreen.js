import React, { useState, useEffect, useCallback } from 'react';
import styled from 'styled-components';
import BackgroundRenderer from './BackgroundRenderer';
import CharacterDisplay from './CharacterDisplay';
import DialogueBoxComponent from './DialogueBox';
import LoadingScreen from './LoadingScreen';
import apiService from '../services/apiService';

const GameContainer = styled.div`
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  user-select: none;
  font-family: 'Arial', sans-serif;
`;

const CharacterLayer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
`;

const GameScreen = ({ storyData, apiKey }) => {
  const [currentStoryData, setCurrentStoryData] = useState(storyData);
  const [currentScriptIndex, setCurrentScriptIndex] = useState(0);
  const [activeCharacters, setActiveCharacters] = useState({});
  const [currentChapterIndex, setCurrentChapterIndex] = useState(1);
  const [isLoadingNext, setIsLoadingNext] = useState(false);
  
  const currentScript = currentStoryData?.scripts[currentScriptIndex];
  const isNarrator = currentScript?.role === 'narrator';
  
  // Handle character positioning logic
  useEffect(() => {
    if (!isNarrator && currentScript) {
      const characterName = currentScript.role;
      const emotion = currentScript.emotion;
      
      // Determine position based on character appearance order
      // First time seeing a character, assign them a position
      setActiveCharacters(prev => {
        const existingPositions = Object.values(prev).map(char => char.position);
        let position = 'left';
        
        if (prev[characterName]) {
          // Character already exists, keep their position but update emotion
          position = prev[characterName].position;
        } else {
          // New character - assign available position
          if (existingPositions.includes('left') && !existingPositions.includes('right')) {
            position = 'right';
          }
        }
        
        // Keep all previously visible characters, but only make current speaker fully visible
        const updatedCharacters = {};
        Object.keys(prev).forEach(name => {
          updatedCharacters[name] = {
            ...prev[name],
            visible: name === characterName
          };
        });
        
        // Add or update the current speaker
        updatedCharacters[characterName] = {
          position,
          emotion,
          visible: true
        };
        
        return updatedCharacters;
      });
    } else if (isNarrator) {
      // For narrator scenes, dim all characters
      setActiveCharacters(prev => {
        const dimmedCharacters = {};
        Object.keys(prev).forEach(name => {
          dimmedCharacters[name] = {
            ...prev[name],
            visible: false
          };
        });
        return dimmedCharacters;
      });
    }
  }, [currentScriptIndex, currentScript, isNarrator]);

  // Function to load next chapter
  const loadNextChapter = useCallback(async () => {
    if (isLoadingNext) return;
    
    setIsLoadingNext(true);
    try {
      const nextChapterData = await apiService.generateScript(currentChapterIndex + 1);
      setCurrentStoryData(nextChapterData);
      setCurrentScriptIndex(0);
      setCurrentChapterIndex(prev => prev + 1);
      setActiveCharacters({}); // Reset characters for new chapter
      console.log(`Loaded chapter ${currentChapterIndex + 1}`);
    } catch (error) {
      console.error('Failed to load next chapter:', error);
      // Could show an error message to the user here
    } finally {
      setIsLoadingNext(false);
    }
  }, [currentChapterIndex, isLoadingNext]);
  
  // Handle click to advance script
  const handleAdvanceScript = useCallback(async () => {
    if (!currentStoryData?.scripts) return;
    
    if (currentScriptIndex < currentStoryData.scripts.length - 1) {
      setCurrentScriptIndex(prev => prev + 1);
    } else {
      // End of current chapter - load next chapter
      await loadNextChapter();
    }
  }, [currentScriptIndex, currentStoryData, loadNextChapter]);
  
  // Handle keyboard and mouse input
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.code === 'Space' || event.code === 'Enter') {
        event.preventDefault();
        handleAdvanceScript();
      }
    };
    
    window.addEventListener('keydown', handleKeyPress);
    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [handleAdvanceScript]);
  
  if (!currentScript && !isLoadingNext) {
    return <div>Loading story...</div>;
  }

  if (isLoadingNext) {
    return <LoadingScreen />;
  }
  
  return (
    <GameContainer onClick={handleAdvanceScript}>
      {/* Background Layer */}
      <BackgroundRenderer scene={currentStoryData?.scene_background || 'castle'} />
      
      {/* Character Layer */}
      <CharacterLayer>
        {Object.entries(activeCharacters).map(([characterName, characterData]) => (
          <CharacterDisplay
            key={characterName}
            characterName={characterName}
            emotion={characterData.emotion}
            position={characterData.position}
            visible={characterData.visible}
          />
        ))}
      </CharacterLayer>
      
      {/* Dialogue Layer */}
      <DialogueBoxComponent
        characterName={currentScript.role}
        script={currentScript.script}
        isNarrator={isNarrator}
      />
    </GameContainer>
  );
};

export default GameScreen;