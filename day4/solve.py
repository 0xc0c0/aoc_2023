#!/usr/bin/env python

"""Python solver file for Advent of Code Day 4"""
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_line(text_line):
    """Parses single line of text from the input file

    Args:
        text_line (str): raw text line from input file
    """
    text_left, text_right = text_line.strip().split("|")
    card_num_text, win_text = text_left.strip().split(":")
    card_num = int(card_num_text.split()[1].strip())
    winning_nums = [int(x) for x in win_text.strip().split()]
    drawn_nums = [int(x) for x in text_right.strip().split()]
    return card_num, winning_nums, drawn_nums


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    cards = [
        parse_line(line.strip()) for line in text_data.strip("\n").strip().split("\n")
    ]
    return cards


def get_points_worth(cards):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    total = 0
    for _, winning_nums, drawn_nums in cards:
        card_winners = 0
        for w in winning_nums:
            if w in drawn_nums:
                card_winners += 1
        if card_winners > 0:
            total += 2 ** (card_winners - 1)

    return total


def get_cards_count(cards):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """

    cards_to_process = [1] * (len(cards) + 1)
    cards_to_process[0] = 0
    winners_count = [0] * (len(cards) + 1)
    total_cards = 0

    for card_num, winning_nums, drawn_nums in cards:
        card_winners = 0
        for w in winning_nums:
            if w in drawn_nums:
                card_winners += 1
        winners_count[card_num] = card_winners

    for i, _ in enumerate(cards_to_process):
        logger.debug("processing card index %d", i)
        while cards_to_process[i] > 0:
            # process a card
            total_cards += 1
            cards_to_process[i] -= 1
            for a in range(winners_count[i]):
                # add a card to process at the offset for the winner
                cards_to_process[i + a + 1] += 1
    return total_cards


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_points_worth(data)
    print(f"Day 4: Part 1: Total Scratchcard Points: {answer}")
    answer2 = get_cards_count(data)
    print(f"Day 4: Part 2: Total Scratchcards: {answer2}")


if __name__ == "__main__":
    main()
