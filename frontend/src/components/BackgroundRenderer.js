import React from 'react';
import styled from 'styled-components';
import { getBackgroundPath } from '../data/mockData';

const BackgroundContainer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
`;

const BackgroundImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: opacity 0.5s ease-in-out;
`;

const FallbackBackground = styled.div`
  width: 100%;
  height: 100%;
  background: ${props => {
    switch(props.scene) {
      case 'castle': return 'linear-gradient(135deg, #6b73ff 0%, #000dff 100%)';
      case 'forest': return 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)';
      case 'village': return 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)';
      case 'dungeon': return 'linear-gradient(135deg, #434343 0%, #000000 100%)';
      default: return 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    }
  }};
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 24px;
  text-transform: capitalize;
`;

const BackgroundRenderer = ({ scene }) => {
  const [imageLoaded, setImageLoaded] = React.useState(false);
  const [imageError, setImageError] = React.useState(false);
  const imageRef = React.useRef(null);
  
  const backgroundPath = getBackgroundPath(scene);
  
  // Check if image is already cached/loaded
  const checkImageStatus = React.useCallback((img) => {
    if (img && (img.complete || img.naturalWidth > 0)) {
      setImageLoaded(true);
      return true;
    }
    return false;
  }, []);
  
  React.useEffect(() => {
    // Reset states when scene changes
    setImageLoaded(false);
    setImageError(false);
    
    // Check if the image is already loaded after a brief delay
    const timeoutId = setTimeout(() => {
      if (imageRef.current && !imageError) {
        if (!checkImageStatus(imageRef.current)) {
          // If image still isn't loaded after timeout, force show it
          setImageLoaded(true);
        }
      }
    }, 1000); // 1 second fallback timeout
    
    return () => clearTimeout(timeoutId);
  }, [scene, checkImageStatus, imageError]);
  
  const handleImageLoad = React.useCallback(() => {
    setImageLoaded(true);
  }, []);
  
  const handleImageError = React.useCallback(() => {
    setImageError(true);
  }, []);
  
  // Check image status when ref is set
  const handleImageRef = React.useCallback((img) => {
    imageRef.current = img;
    if (img) {
      // Check immediately if image is already cached
      checkImageStatus(img);
    }
  }, [checkImageStatus]);
  
  return (
    <BackgroundContainer>
      {!imageError ? (
        <BackgroundImage
          ref={handleImageRef}
          src={backgroundPath}
          alt={`${scene} background`}
          onLoad={handleImageLoad}
          onError={handleImageError}
          style={{ opacity: imageLoaded ? 1 : 0 }}
        />
      ) : (
        <FallbackBackground scene={scene}>
          {scene} Background
        </FallbackBackground>
      )}
    </BackgroundContainer>
  );
};

export default BackgroundRenderer;