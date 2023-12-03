#!/usr/bin/env python

"""Python solver file for Advent of Code Day 2"""
import os
import logging
import math

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_bag(bag_text):
    """Parse bag within a round

    Args:
        bag_text (str): bag text

    Returns:
        dict: color (key) and cube count (value)
    """
    cube_count, bag_color = bag_text.strip().split()
    cube_count = int(cube_count)
    return (bag_color, cube_count)


def parse_round(round_text):
    """Parse round within the text list of rounds

    Args:
        round_text (str): round text

    Returns:
        list: parsed bags composing the round
    """
    bags = [parse_bag(x) for x in round_text.strip().split(",")]
    bags = {k: v for (k, v) in bags}
    return bags


def parse_line(text_line):
    """Parses single line of text from the input file

    Args:
        text_line (str): raw text line from input file
    """
    # logger.debug("split text_line is %s", text_line.strip().split(":"))
    # logger.debug("length: %d", len(text_line.strip().split(":")))
    game_text, rounds_text = text_line.strip().split(":")
    game_index = int(game_text.strip().split()[1])
    rounds = [parse_round(round_text) for round_text in rounds_text.strip().split(";")]
    return (game_index, rounds)


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    data = [parse_line(line) for (line) in text_data.strip().strip("\n").split("\n")]
    new_data = {k: v for (k, v) in data}
    logger.debug(new_data)
    return new_data


def get_possible_games_sum(data):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    maxes = {"red": 12, "green": 13, "blue": 14}

    all_games = set(data.keys())
    impossible = set()

    for game_number, game_rounds in data.items():
        for game_round in game_rounds:
            for bag_color, cubes in game_round.items():
                if cubes > maxes[bag_color]:
                    impossible.add(game_number)

    possible = all_games - impossible
    return sum(possible)


def get_power(game_rounds):
    """get power for Part 2

    Args:
        game_rounds (list): list of dicts representing parsed game rounds

    Returns:
        int: product of maximums found in each color across all game rounds
    """
    maxes = {"red": 0, "green": 0, "blue": 0}

    for game_round in game_rounds:
        for bag_color, cubes in game_round.items():
            if cubes > maxes[bag_color]:
                maxes[bag_color] = cubes

    return math.prod(maxes.values())


def get_min_power_sum(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """

    powers = [get_power(v) for (k, v) in data.items()]
    return sum(powers)


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_possible_games_sum(data)
    print(f"Day 2: Part 1: Get Possible Games: {answer}")
    answer2 = get_min_power_sum(data)
    print(f"Day 2: Part 2: Get Sum of Powers: {answer2}")


if __name__ == "__main__":
    main()
