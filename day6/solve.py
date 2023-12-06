#!/usr/bin/env python

"""Python solver file for Advent of Code Day 6"""
import os
import math
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


# def parse_line(text_line):
#     """Parses single line of text from the input file

#     Args:
#         text_line (str): raw text line from input file
#     """
#     return list(text_line)


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    text_time, text_distance = text_data.strip().strip("\n").split("\n")
    times = [int(t) for t in text_time.split(":")[1].strip().split()]
    distances = [int(d) for d in text_distance.split(":")[1].strip().split()]
    return times, distances


def parse_data2(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    text_time, text_distance = text_data.strip().strip("\n").split("\n")
    time = int(text_time.split(":")[1].strip().replace(" ", ""))
    distance = int(text_distance.split(":")[1].strip().replace(" ", ""))
    return time, distance


def get_race_winners(time, distance):
    """Find race winners for a (time, distance) race

    Args:
        time (int): time alloted for race in ms
        distance (int): current record distance for race

    Returns:
        int: possible unique whole number (ms) charge times that result in a record breaker
    """
    count = 0
    for s in range(time):
        if s * (time - s) > distance:
            count += 1
    return count


def find_wins(times, distances):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    counts = [get_race_winners(t, d) for t, d in zip(times, distances)]
    return math.prod(counts)


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = find_wins(*data)
    print(f"Day 6: Part 1: Find possible winners: {answer}")
    data = parse_data2(text_data)
    answer2 = get_race_winners(*data)
    print(f"Day 6: Part 2: Find possible winners (large number): {answer2}")


if __name__ == "__main__":
    main()
