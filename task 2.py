from pprint import pprint
import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()

pprint(game_stamps)


def get_score(game_stamps, offset):
    '''
    Takes a list of game's stamps and a time offset and returns the scores for the home and away teams.
    Please note that for some offsets, the game_stamps list may not contain scores.
    '''

    # Iterate over the stamps to find the closest stamp with an offset less than or equal to the target offset
    for stamp in reversed(game_stamps):
        if stamp["offset"] <= offset:
            return stamp["score"]["home"], stamp["score"]["away"]

    # If no suitable stamp is found, return None
    return None, None

import unittest

class TestGetScoreFunction(unittest.TestCase):

    def test_offset_before_game_starts(self):
        game_stamps = [{"offset": 0, "score": {"home": 0, "away": 0}}]
        home_score, away_score = get_score(game_stamps, -1)
        self.assertIsNone(home_score)
        self.assertIsNone(away_score)

    def test_offset_at_game_start(self):
        game_stamps = [{"offset": 0, "score": {"home": 0, "away": 0}}]
        home_score, away_score = get_score(game_stamps, 0)
        self.assertEqual(home_score, 0)
        self.assertEqual(away_score, 0)

    def test_offset_during_game(self):
        game_stamps = [{"offset": 0, "score": {"home": 0, "away": 0}},
                       {"offset": 10, "score": {"home": 1, "away": 0}},
                       {"offset": 20, "score": {"home": 1, "away": 1}}]
        home_score, away_score = get_score(game_stamps, 15)
        self.assertEqual(home_score, 1)
        self.assertEqual(away_score, 0)

    def test_offset_after_game_ends(self):
        game_stamps = [{"offset": 0, "score": {"home": 0, "away": 0}},
                       {"offset": 10, "score": {"home": 1, "away": 0}},
                       {"offset": 20, "score": {"home": 1, "away": 1}}]
        home_score, away_score = get_score(game_stamps, 25)
        self.assertEqual(home_score, 1)
        self.assertEqual(away_score, 1)

if __name__ == '__main__':
    unittest.main()