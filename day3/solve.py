#!/usr/bin/env python

"""Python solver file for Advent of Code Day 3"""
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

VALID_SYMBOLS = {"-", "#", "%", "+", "&", "*", "=", "@", "/", "$"}


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_line(rownum, text_line):
    """Parses single line of text from the input file

    Args:
        text_line (str): raw text line from input file
        rownum (int): index of line being processed
    """
    numbers = []
    symbols = []
    text_line = text_line.strip()

    # process symbols first
    for j, c in enumerate(text_line):
        if c in VALID_SYMBOLS:
            symbols.append({"sym": c, "i": rownum, "j": j})

    # process numbers next, ignoring symbols
    # for c in VALID_SYMBOLS:
    #     text_line = text_line.replace(c, ".")
    # logger.debug("text_line without symbols: %s", text_line)

    start_index = 0
    while start_index < len(text_line):
        if not text_line[start_index].isdigit():
            start_index += 1
        else:
            end_index = start_index + 1
            while end_index < len(text_line) and text_line[end_index].isdigit():
                end_index += 1
            num = int(text_line[start_index:end_index])
            numbers.append({"num": num, "i": rownum, "j": start_index})
            start_index = end_index

    return (numbers, symbols)


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        numbers: list of numbers and their locations in the schematic
        symbols: list of symbols and their locations in the schematics
    """
    lines_data = [
        parse_line(i, line)
        for i, line in enumerate(text_data.strip().strip("\n").split("\n"))
    ]
    numbers = list()
    symbols = list()
    for nums, syms in lines_data:
        if nums:
            numbers = numbers + nums
        if syms:
            symbols = symbols + syms
    # numbers = list(filter([].__ne__, numbers))
    # symbols = list(filter([].__ne__, symbols))
    logger.debug("numbers: %s", numbers)
    logger.debug("symbols: %s", symbols)
    return numbers, symbols


def get_part_number_sum(numbers, symbols):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    # check numbers for adjacency and add to valid list
    parts = list()
    for n in numbers:
        endj = n["j"] + len(str(n["num"])) - 1
        for s in symbols:
            if s["i"] >= n["i"] - 1 and s["i"] <= n["i"] + 1:
                if s["j"] >= n["j"] - 1 and s["j"] <= endj + 1:
                    logger.debug(
                        "matched %d at (%d, %d) to %s at (%d, %d)",
                        n["num"],
                        n["i"],
                        n["j"],
                        s["sym"],
                        s["i"],
                        s["j"],
                    )
                    parts.append(n["num"])
                    break

    return sum(parts)


def get_gear_ratio_sum(numbers, symbols):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    gears = list()
    for s in symbols:
        adjacent_numbers = list()
        for n in numbers:
            endj = n["j"] + len(str(n["num"]))
            if (
                s["i"] >= n["i"] - 1
                and s["i"] <= n["i"] + 1
                and s["j"] >= n["j"] - 1
                and s["j"] <= endj
            ):
                logger.debug("appending %d", n["num"])
                adjacent_numbers.append(n["num"])
        if len(adjacent_numbers) == 2:
            gears.append(adjacent_numbers[0] * adjacent_numbers[1])

    return sum(gears)


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    numbers, symbols = parse_data(text_data)
    answer = get_part_number_sum(numbers, symbols)
    print(f"Day 3: Part 1: Sum of All Part Numbers: {answer}")
    answer2 = get_gear_ratio_sum(numbers, symbols)
    print(f"Day 3: Part 2: Sum of All Gear Ratios: {answer2}")


if __name__ == "__main__":
    main()
