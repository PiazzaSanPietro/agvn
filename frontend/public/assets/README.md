# SYSE Visual Novel Assets

This folder contains all the visual assets for the SYSE Visual Novel prototype.

## Directory Structure

```
assets/
├── backgrounds/
│   ├── castle.jpg          # Castle background
│   ├── forest.jpg          # Forest background  
│   ├── village.jpg         # Village background
│   └── dungeon.jpg         # Dungeon background
├── characters/
│   ├── princess_seraphina/
│   │   ├── neutral.png     # Basic expressions
│   │   ├── smile.png
│   │   ├── laugh.png
│   │   ├── ecstatic.png
│   │   ├── gloomy.png
│   │   ├── crying.png
│   │   ├── sobbing.png
│   │   ├── annoyed.png
│   │   ├── angry.png
│   │   ├── rage.png
│   │   ├── puzzled.png     # Complex expressions
│   │   ├── startled.png
│   │   ├── shy.png
│   │   ├── embarrassed.png
│   │   ├── affection.png
│   │   ├── suspicious.png
│   │   ├── smirk.png
│   │   └── thinking.png
│   ├── captain_valerius/
│   │   └── [same emotion files]
│   ├── archmage_lyra/
│   │   └── [same emotion files]
│   ├── deadpool/
│   │   └── [same emotion files]
│   └── demon_soldier/
│       └── [same emotion files]
```

## Asset Requirements

### Background Images
- Resolution: 1920x1080 (16:9 ratio)
- Format: JPG or PNG
- Style: High fantasy, consistent art style

### Character Images
- Resolution: 400x600 recommended
- Format: PNG with transparency
- Style: Visual novel character sprites
- Positioning: Characters should be positioned to appear naturally when displayed on left/right sides

## Adding New Assets

1. Place background images in `backgrounds/` folder
2. Create character folders using lowercase names with underscores
3. Add all emotion variants for each character
4. Update the emotion mapping in the code if adding new emotions

## Placeholder System

The application includes an automatic placeholder system that generates colored rectangles with character names when image assets are not available. This allows the prototype to function even without complete art assets.

## Asset Loading

- Images are loaded asynchronously
- Fallback placeholders are generated automatically
- Error handling prevents crashes from missing assets
- Smooth transitions between character emotions and scenes