"""Python test file for unit testing in support of AoC solves"""
import os
import pytest
from .solve import parse_data, function, function2


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


# @pytest.fixture(name="test_data2")
# def get_test_data_2():
#     """Provides test data using text2.txt for return of file to consume

#     Returns:
#         str: data blob of text from file
#     """
#     # dynamically obtain full path of 'test.txt'
#     test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test2.txt")
#     with open(test_file, "r", encoding="utf-8") as f:
#         text = f.read()
#     return text


def test_parse_input(test_data):
    """Test all parsing functions associated with Part 1

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    tiles, start = data
    assert tiles.shape == (11, 11)
    assert start == (5, 5)


def test_all(test_data):
    """Test all functions associated with Parts 1 and 2

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    tiles, start = data
    assert function(tiles, start, steps=6) == 16
    assert function(tiles, (0, 0), steps=20) == 50
    # assert function(tiles, start, steps=50) == 1594
    # assert function(tiles, start, steps=100) == 6536
    # assert function(tiles, start, steps=500) == 167004
    # assert function(tiles, start, steps=1000) == 668697
    # assert function(tiles, start, steps=5000) == 16733044
    assert function2(tiles) == 0
