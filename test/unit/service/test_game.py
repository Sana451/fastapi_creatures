import pytest
from service import game

word = "bigfoot"
guesses = [
    ("bigfoot", "HHHHHHH"),
    ("abcdefg", "MCMMMCC"),
    ("toofgib", "CCCHCCC"),
    ("wronglength", ""),
    ("", ""),
]


@pytest.mark.parametrize("guess,score", guesses)
def test_match(guess, score):
    assert game.get_score(word, guess) == score


def test_match_simple():
    assert game.get_score("bigfoot", "HHHHHHH") == 'MMMMMMM'


def test_match_simple2():
    assert game.get_score("bigfoot", "abcdefg") == 'MCMMMCC'
