from .pattern_grid import PatternGridGenerator
from .number_sequence import NumberSequenceGenerator
from .memory_cards import MemoryCardsGenerator

# Словарь для получения генератора по имени
GENERATORS = {
    'PatternGridGenerator': PatternGridGenerator,
    'NumberSequenceGenerator': NumberSequenceGenerator,
    'MemoryCardsGenerator': MemoryCardsGenerator,
}