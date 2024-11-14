import random

# Predefined list of descriptions for short-haired and long-haired animals
SHORT_HAIR_DESCRIPTIONS = [
    "This short-haired animal moves with effortless grace, its sleek coat reflecting its practical nature.",
    "A practical and agile creature, its short hair keeps it cool and easy to maintain.",
    "With a smooth and shiny short coat, this animal is both sleek and quick, built for efficiency.",
    "Its short hair highlights a sharp, energetic personality—perfect for action and adventure.",
    "A compact and clean animal, its short fur allows for fast movement and agility.",
    "This animal’s short coat adds to its streamlined, agile form, perfect for navigating tight spaces.",
]

LONG_HAIR_DESCRIPTIONS = [
    "This long-haired animal carries its elegant fur like a royal cloak, flowing and full of warmth.",
    "A majestic presence, its long hair gives it a soft, comforting appearance that is both beautiful and serene.",
    "With luxurious fur flowing behind it, this animal embodies grace and warmth, a sight to behold.",
    "Its flowing mane speaks of beauty and elegance, offering a sense of calm and warmth to all who approach.",
    "This long-haired animal exudes an air of sophistication, its coat rippling with every movement.",
    "Elegant and dignified, this animal's long fur gives it a sense of regality and grace.",
]


# Fallback description function
def get_fallback_description(is_short_hair: bool) -> str:
    """Randomly select a fallback description from the predefined lists."""
    if is_short_hair:
        return random.choice(SHORT_HAIR_DESCRIPTIONS)
    else:
        return random.choice(LONG_HAIR_DESCRIPTIONS)
