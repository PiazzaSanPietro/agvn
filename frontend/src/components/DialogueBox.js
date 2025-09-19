import React from 'react';
import styled from 'styled-components';

const DialogueContainer = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 2;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.8) 30%, rgba(0, 0, 0, 0.95) 100%);
  padding: 40px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
`;

const DialogueBox = styled.div`
  background: rgba(0, 0, 0, 0.85);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 15px;
  padding: 25px 30px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
`;

const CharacterName = styled.div`
  color: ${props => props.isNarrator ? '#ffffff' : '#ffd700'};
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  ${props => props.isNarrator && `
    text-align: center;
    font-style: italic;
    color: #cccccc;
  `}
`;

const DialogueText = styled.div`
  color: #ffffff;
  font-size: 16px;
  line-height: 1.6;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
  ${props => props.isNarrator && `
    text-align: center;
    font-style: italic;
    color: #e0e0e0;
  `}
`;

const ContinueIndicator = styled.div`
  position: absolute;
  bottom: 10px;
  right: 20px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 12px;
  animation: blink 1.5s infinite;
  
  @keyframes blink {
    0%, 50% { opacity: 0.7; }
    51%, 100% { opacity: 0.3; }
  }
`;

const DialogueBoxComponent = ({ characterName, script, isNarrator = false }) => {
  const displayName = isNarrator ? "Narrator" : characterName;
  
  return (
    <DialogueContainer>
      <DialogueBox>
        <CharacterName isNarrator={isNarrator}>
          {displayName}
        </CharacterName>
        <DialogueText isNarrator={isNarrator}>
          {script}
        </DialogueText>
        <ContinueIndicator>
          ▼ Click to continue
        </ContinueIndicator>
      </DialogueBox>
    </DialogueContainer>
  );
};

export default DialogueBoxComponent;