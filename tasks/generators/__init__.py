from .pattern_grid import PatternGridGenerator
from .number_sequence import NumberSequenceGenerator
from .memory_cards import MemoryCardsGenerator
from .blind_arithmetic import BlindArithmeticGenerator
from .number_position import NumberPositionGenerator
from .word_recall import WordRecallGenerator
from .color_grid import ColorGridGenerator
from .odd_word import OddWordGenerator

GENERATORS = {
    'PatternGridGenerator': PatternGridGenerator,
    'NumberSequenceGenerator': NumberSequenceGenerator,
    'MemoryCardsGenerator': MemoryCardsGenerator,
    'BlindArithmeticGenerator': BlindArithmeticGenerator,
    'NumberPositionGenerator': NumberPositionGenerator,
    'WordRecallGenerator': WordRecallGenerator,
    'ColorGridGenerator': ColorGridGenerator,
    'OddWordGenerator': OddWordGenerator
}