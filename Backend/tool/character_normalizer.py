"""
Character Name Normalization Utility

This module provides functionality to standardize character names from the story generation system.
It handles various inconsistencies like titles, case variations, and Korean translations.

Key Features:
- Comprehensive character mapping for all characters in base_world.prompt
- Case-insensitive matching
- Korean language support
- Safe fallback: preserves original names if no mapping found
- Zero data loss architecture

Usage:
    from tool.character_normalizer import normalize_character_name
    
    standardized_name = normalize_character_name("Princess Seraphina")
    # Returns: "Seraphina"
"""

# --- Character Name Mappings ---

# Comprehensive mapping dictionary for all characters
# Format: {variation: standardized_name}
CHARACTER_MAPPINGS = {
    # Hero Characters
    # Seraphina variations
    "강지훈": "강지훈",
    "지훈": "강지훈",
    "kang ji-hoon": "강지훈",
    "ji-hoon": "강지훈",
    "윤서아": "윤서아",
    "서아": "윤서아",
    "yoon seo-ah": "윤서아",
    "seo-ah": "윤서아",
    "박민지": "박민지",
    "민지": "박민지",
    "park min-ji": "박민지",
    "min-ji": "박민지",
    "김태성": "김태성",
    "태성": "김태성",
    "kim tae-sung": "김태성",
    "kim tae-seong": "김태성",
    "tae-sung": "김태성",
    "정미연": "정미연",
    "미연": "정미연",
    "jeong mi-yeon": "정미연",
    "mi-yeon": "정미연",

    # System Characters
    "narrator": "Narrator",
    "Narrator": "Narrator",
    "내레이터": "Narrator",
    "나레이터": "Narrator",
    "나레이션": "Narrator",
    "system": "Narrator",
}


def normalize_character_name(character_name: str) -> str:
    """
    Normalize character name to standardized form.
    
    This function takes a character name (which may include titles, different cases,
    or Korean translations) and returns the standardized character name.
    
    If the character name is not found in the mapping, the original name is returned
    unchanged to ensure no data loss.
    
    Args:
        character_name (str): The original character name from the database
        
    Returns:
        str: The standardized character name, or original name if not found in mapping
        
    Examples:
        >>> normalize_character_name("Princess Seraphina")
        'Seraphina'
        >>> normalize_character_name("세라피나")
        'Seraphina'
        >>> normalize_character_name("Unknown Character")
        'Unknown Character'
    """
    if not character_name or not isinstance(character_name, str):
        return character_name
    
    # Convert to lowercase for case-insensitive matching
    lowercase_name = character_name.lower().strip()
    
    # If after stripping we have an empty string, return original
    if not lowercase_name:
        return character_name
    
    # Direct mapping lookup
    if lowercase_name in CHARACTER_MAPPINGS:
        return CHARACTER_MAPPINGS[lowercase_name]
    
    # Substring matching for partial matches
    # This handles cases like "Princess Seraphina Elara" matching "seraphina"
    for mapping_key, standardized_name in CHARACTER_MAPPINGS.items():
        if mapping_key in lowercase_name or lowercase_name in mapping_key:
            return standardized_name
    
    # Fallback: return original name unchanged
    return character_name


def get_all_standardized_characters() -> list:
    """
    Get list of all standardized character names.
    
    Returns:
        list: List of unique standardized character names
    """
    return list(set(CHARACTER_MAPPINGS.values()))


def get_character_variations(standardized_name: str) -> list:
    """
    Get all variations for a given standardized character name.
    
    Args:
        standardized_name (str): The standardized character name
        
    Returns:
        list: List of all variations that map to this standardized name
    """
    variations = []
    for variation, standard in CHARACTER_MAPPINGS.items():
        if standard == standardized_name:
            variations.append(variation)
    return variations