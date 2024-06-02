from typing import Tuple, Dict

from settings import *


def parse_str(values: Tuple, str_format="%s"):
    return tuple(str_format % v for v in values)


class Options:
    N_ATTR = "n_attributes"
    N_ATTR_V = "n_attribute_values"
    CARD_QL = "card_quality"
    GAME_TM = "game_time"
    SET_SCORE = "set_score"
    END_GUESS_SCORE = "end_guess_score"
    INTERSET_SCORE = "interset_score"
    COMET_SCORE = "comet_score"
    PLANET_SCORE = "planet_score"
    WITH_BORDER = False

    OPTION_VALUES: Dict[str, Tuple] = {
        N_ATTR: ("Nº Attributes", (2, 3, 4), "%s"),
        N_ATTR_V: ("Nº Attribute Values", (3, 5), "%s"),
        CARD_QL: ("Card Quality", (1, 2, 3, 4), "%s"),
        GAME_TM: ("Game Time", (60, 180, 240, 300), "%s"),
        SET_SCORE: ("SET Score", (75, 150, 300, 600), "%sp"),
        END_GUESS_SCORE: ("End Guess Score", (250, 500, 750, 900), "%sp"),
        INTERSET_SCORE: ("Interset Score", (100, 300, 600, 700), "%sp"),
        PLANET_SCORE: ("Planet Score", (300, 600, 900, 1200), "%sp"),
        COMET_SCORE: ("Comet Score", (700, 900, 1200, 1800), "%sp"),
        WITH_BORDER: ("Card Border", (True, False), "%s")
    }


SET_GAME_DESCRIPTION = """
    The Objective of the Game
    is finding three or five
    cards (depending on the
    number of values per
    feature) such that
    the cards are a SET.

    For three cards to
    form a SET, each of the
    four features must be
    either:

    All the same on each card
    All different on each card
"""
END_GAME_DESCRIPTION = """
    Description of the game
"""
INTERSET_GAME_DESCRIPTION = """
    Description of the game
"""
SPC_GAME_DESCRIPTION = """
    Description of the game
"""
STRUCTURE_DESCRIPTION = """
    Description of the game
"""


class Modes:
    SET_GAME = "set_game"
    END_GAME = "end_game"
    INTERSET_GAME = "interset_game"
    SPC_GAME = "set-planet-comet"
    STRUCTURE_DRAW = "structure_draw"
    # Gamemodes
    APP_MODES: Dict = {
        SET_GAME: {
            "name": "The Game of SET",
            "instructions": SET_GAME_DESCRIPTION,
            "options": {
                Options.N_ATTR: 4,
                Options.N_ATTR_V: 3,
                Options.GAME_TM: 240,
                Options.CARD_QL: 2,
                Options.SET_SCORE: 300,
            },
        },
        END_GAME: {
            "name": "End Game",
            "instructions": END_GAME_DESCRIPTION,
            "options": {
                Options.N_ATTR: 4,
                Options.N_ATTR_V: 3,
                Options.GAME_TM: 240,
                Options.CARD_QL: 2,
                Options.SET_SCORE: 300,
                Options.END_GUESS_SCORE: 250,
            },
        },
        INTERSET_GAME: {
            "name": "Interset Game",
            "instructions": INTERSET_GAME_DESCRIPTION,
            "options": {
                Options.N_ATTR: 4,
                Options.N_ATTR_V: 3,
                Options.GAME_TM: 240,
                Options.CARD_QL: 2,
                Options.INTERSET_SCORE: 300,
            },
        },
        SPC_GAME: {
            "name": "SET-Planet-Comet",
            "instructions": SPC_GAME_DESCRIPTION,
            "options": {
                Options.N_ATTR: 4,
                Options.N_ATTR_V: 3,
                Options.GAME_TM: 240,
                Options.CARD_QL: 2,
                Options.SET_SCORE: 300,
                Options.COMET_SCORE: 700,
                Options.PLANET_SCORE: 300,
            },
        },
        STRUCTURE_DRAW: {
            "name": "Structure Draw",
            "instructions": STRUCTURE_DESCRIPTION,
            "options": {
                Options.N_ATTR: 4,
                Options.N_ATTR_V: 3,
                Options.CARD_QL: 2,
                Options.WITH_BORDER: False
            }
        },
    }

    @classmethod
    def get_selection_options(cls, game_id: str):
        if game_id not in cls.APP_MODES:
            return {}
        opt_values = Options.OPTION_VALUES
        return {
            opt_id: (
                opt_values[opt_id][0],
                parse_str(opt_values[opt_id][1], opt_values[opt_id][2]),
                opt_values[opt_id][1],
                value,
            )
            for opt_id, value in cls.APP_MODES[game_id]["options"].items()
        }
