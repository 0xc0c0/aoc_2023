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

@pytest.fixture
def test_data2():
    #dynamically obtain full path of 'test.txt'
    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test2.txt')
    with open(test_file, 'r') as f:
        text = f.read()
    return text

def test_parse_input(test_data):
    calibration_lines = parse_data(test_data)
    assert get_cal_val(calibration_lines[0]) == 12
    assert get_cal_val(calibration_lines[3]) == 77
    
def test_parse_input_2(test_data2):
    calibration_lines = parse_data(test_data2)
    assert get_cal_val_part2(calibration_lines[0]) == 29
    assert get_cal_val_part2(calibration_lines[3]) == 24
    
  
def test_all(test_data):
    grid = parse_data(test_data)
