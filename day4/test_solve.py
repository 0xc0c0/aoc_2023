"""Python test file for unit testing in support of AoC solves"""
import os
import pytest
from .solve import parse_data, get_points_worth, get_cards_count


@pytest.fixture(name="test_data")
def get_test_data_1():
    """Provides test data using text.txt for return of file to consume

    Returns:
        str: data blob of text from file
    """
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test.txt")
    with open(test_file, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def test_parse_input(test_data):
    """Test all parsing functions associated with Part 1

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    assert (len(data)) == 6
    assert data[0][0] == 1  # card 1
    assert data[2][0] == 3  # card 3
    assert data[2][1][2] == 53  # 3rd winning number on card 3


def test_all(test_data):
    """Test all functions associated with Parts 1 and 2

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    assert get_points_worth(data) == 13
    assert get_cards_count(data) == 30
