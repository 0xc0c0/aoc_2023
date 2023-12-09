"""Python test file for unit testing in support of AoC solves"""
import os
import pytest
from .solve import parse_data, get_min_required_steps, get_min_required_ghost_steps


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


@pytest.fixture(name="test_data2")
def get_test_data_2():
    """Provides test data using text2.txt for return of file to consume

    Returns:
        str: data blob of text from file
    """
    # dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test2.txt")
    with open(test_file, "r", encoding="utf-8") as f:
        text = f.read()
    return text


@pytest.fixture(name="test_data3")
def get_test_data_3():
    """Provides test data using text3.txt for return of file to consume

    Returns:
        str: data blob of text from file
    """
    # dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test3.txt")
    with open(test_file, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def test_parse_input(test_data, test_data2):
    """Test all parsing functions associated with Part 1

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    instructions, network = data
    assert len(instructions) == 2
    assert len(network) == 7

    data = parse_data(test_data2)
    instructions, network = data
    assert len(instructions) == 3
    assert len(network) == 3


def test_all(test_data, test_data2, test_data3):
    """Test all functions associated with Parts 1 and 2

    Args:
        test_data (str): takes in a raw text str object as a data blob
    """
    data = parse_data(test_data)
    assert get_min_required_steps(data) == 2

    data2 = parse_data(test_data2)
    assert get_min_required_steps(data2) == 6

    data3 = parse_data(test_data3)
    assert get_min_required_ghost_steps(data3) == 6
