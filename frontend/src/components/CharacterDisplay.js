import React from 'react';
import styled from 'styled-components';
import { getCharacterSpritePath } from '../data/mockData';

const CharacterContainer = styled.div`
  position: absolute;
  bottom: 0;
  height: 75%;
  z-index: 1;
  ${props => props.position === 'left' ? 'left: 5%;' : 'right: 5%;'}
  display: flex;
  align-items: flex-end;
  opacity: ${props => props.visible ? 1 : 0};
  transition: all 0.5s ease-in-out;
  transform: scale(${props => props.visible ? props.scale || 1.2 : 0.95});
  transform-origin: bottom center;
  pointer-events: ${props => props.visible ? 'auto' : 'none'};
`;

const CharacterSprite = styled.img`
  height: 100%;
  width: auto;
  object-fit: cover;
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
  transition: opacity 0.3s ease-in-out;
`;

const CharacterPlaceholder = styled.div`
  width: 400px;
  height: 600px;
  background: ${props => {
    // Generate color based on character name hash
    let hash = 0;
    for (let i = 0; i < props.characterName.length; i++) {
      hash = props.characterName.charCodeAt(i) + ((hash << 5) - hash);
    }
    const color = Math.abs(hash) % 16777215;
    return `#${color.toString(16).padStart(6, '0')}`;
  }};
  opacity: 0.7;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  text-align: center;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
`;

const CharacterDisplay = ({ characterName, emotion, position, visible = true, scale = 1.2 }) => {
  const [spriteLoaded, setSpriteLoaded] = React.useState(false);
  const [spriteError, setSpriteError] = React.useState(false);
  const [currentSpritePath, setCurrentSpritePath] = React.useState(null);
  
  const spritePath = getCharacterSpritePath(characterName, emotion);
  
  React.useEffect(() => {
    if (spritePath && spritePath !== currentSpritePath) {
      setCurrentSpritePath(spritePath);
      setSpriteLoaded(false);
      setSpriteError(false);
    }
  }, [spritePath, currentSpritePath]);
  
  const handleSpriteLoad = () => {
    setSpriteLoaded(true);
  };
  
  const handleSpriteError = () => {
    setSpriteError(true);
  };
  
  // Don't render anything for narrator or if character name is null
  if (!characterName || characterName === 'narrator') {
    return null;
  }
  
  return (
    <CharacterContainer position={position} visible={visible} scale={scale}>
      {currentSpritePath && !spriteError ? (
        <CharacterSprite
          src={currentSpritePath}
          alt={`${characterName} - ${emotion}`}
          onLoad={handleSpriteLoad}
          onError={handleSpriteError}
          style={{ opacity: spriteLoaded ? 1 : 0 }}
        />
      ) : (
        <CharacterPlaceholder characterName={characterName}>
          <div>
            <div>{characterName}</div>
            <div style={{ fontSize: '14px', marginTop: '10px' }}>
              {emotion}
            </div>
          </div>
        </CharacterPlaceholder>
      )}
    </CharacterContainer>
  );
};

export default CharacterDisplay;