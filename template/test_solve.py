import pytest
import os
from .solve import *

@pytest.fixture
def test_data():
    #dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test.txt')
    with open(test_file, 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    grid = parse_data(test_data)
    assert type(grid) == np.ndarray
    assert grid[1,3] == 5
    assert grid.ndim == 2
    assert grid.shape == (10,10)
  
def test_all(test_data):
    grid = parse_data(test_data)
