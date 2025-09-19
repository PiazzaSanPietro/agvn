// Mock data service for visual novel
// Based on the JSON structure from response_text.log

export const sampleStoryData = {
  scene_background: "castle",
  scripts: [
    {
      role: "narrator",
      emotion: "neutral",
      script: "Once upon a time in a land far, far away..."
    }
  ]
};

// Character name mapping to asset folders
export const characterMapping = {
  // Full names (from mock data)
  "강지훈": "강지훈",
  "윤서아": "윤서아",
  "박민지": "박민지",
  "김태성": "김태성",
  "정미연": "정미연",

  "Narrator": "narrator"
};

// Available emotions for character sprites
export const availableEmotions = [
  "neutral", "happy", "laugh", "sad", "angry", "surprised", "shy"
];

// Background scenes mapping
export const backgroundMapping = {
  "Classroom_Day": "Classroom_Day.png",
  "Classroom_Sunset": "Classroom_Sunset.png",
  "School_Hallway_Day": "School_Hallway_Day.png",
  "School_Rooftop": "School_Rooftop.png",
  "Protagonist_Room": "Protagonist_Room.png",
  "Cafe_Interior": "Cafe_Interior.png",
  "Park": "Park.png",
  "Schoolyard": "Schoolyard.png"
};

// Asset path utilities
export const getCharacterSpritePath = (characterName, emotion) => {
  const assetFolder = characterMapping[characterName];
  if (!assetFolder) return null;
  
  return `/assets/characters/${assetFolder}/${emotion}.png`;
};

export const getBackgroundPath = (sceneName) => {
  const backgroundFile = backgroundMapping[sceneName];
  if (!backgroundFile) return "/assets/backgrounds/castle.png"; // Default fallback
  
  return `/assets/backgrounds/${backgroundFile}`;
};