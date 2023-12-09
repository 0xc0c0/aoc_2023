#!/usr/bin/env python

"""Python solver file for Advent of Code Day 7"""
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
    text_cards, text_bid = text_line.strip().split()
    hand = list(text_cards.strip())
    bid = int(text_bid.strip())
    return (hand, bid)


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    data = [
        parse_line(line.strip()) for line in text_data.strip().strip("\n").split("\n")
    ]
    return data


def get_hand_type(cards):
    """return a 1-7 type of camel poker hand

    Args:
        cards (list): list of cards from a camel poker hand

    Returns:
        _type_: _description_
    """
    pairs = set()
    three_of_a_kind = False
    for card in cards:
        if cards.count(card) == 5:
            return 7  # five of a kind
        if cards.count(card) == 4:
            return 6  # four of a kind
        if cards.count(card) == 3:
            three_of_a_kind = True
        elif cards.count(card) == 2:
            pairs.add(card)

    if three_of_a_kind:
        if len(pairs) == 1:
            return 5  # full house
        else:
            return 4  # three of a kind
    elif len(pairs) == 2:
        return 3  # two pair
    elif len(pairs) == 1:
        return 2  # one pair
    else:
        return 1  # high card


def get_hand_type_2(cards):
    """return a 1-7 type of camel poker hand

    Args:
        cards (list): list of cards from a camel poker hand

    Returns:
        _type_: _description_
    """
    pairs = set()
    three_of_a_kind = False
    joker_count = cards.count("J")
    for card in cards:
        if card == "J":
            continue

        if (cards.count(card) + joker_count) == 5:
            return 7  # five of a kind including wilds
        if (cards.count(card) + joker_count) == 4:
            return 6  # four of a kind including wilds
        if cards.count(card) == 3:
            three_of_a_kind = True
        elif cards.count(card) == 2:
            pairs.add(card)

    # at this point, we know how many jokers we have, three-of-a-kinds
    # that are non-joker, and pairs that are non-joker
    if joker_count == 5:
        return 7  # five of a kind
    if joker_count == 2:
        return 4  # three of a kind
    if joker_count == 1:
        if len(pairs) == 2:
            return 5  # full house
        if len(pairs) == 1:
            return 4  # three of a kind
        if len(pairs) == 0:
            return 2  # one pair

    # no jokers!
    if three_of_a_kind:
        if len(pairs) == 1:
            return 5  # full house
        else:
            return 4  # three of a kind
    if len(pairs) == 2:
        return 3  # two pair
    if len(pairs) == 1:
        return 2  # one pair

    return 1  # high card


def get_card_value(card):
    """return nominal value of individual camel poker card

    Args:
        card (chr)): card ASCII char

    Returns:
        int: 2-14 value based on card (2-A, respectively)
    """
    if card.isdigit():
        return int(card)
    else:
        if card == "T":
            return 10
        elif card == "J":
            return 11
        elif card == "Q":
            return 12
        elif card == "K":
            return 13
        elif card == "A":
            return 14

    logger.info("should never reach here!")
    return 15


def get_card_value_2(card):
    """return nominal value of individual camel poker card

    Args:
        card (chr)): card ASCII char

    Returns:
        int: 2-14 value based on card (2-A, respectively)
    """
    if card.isdigit():
        return int(card)
    else:
        if card == "T":
            return 10
        elif card == "J":
            return 1
        elif card == "Q":
            return 12
        elif card == "K":
            return 13
        elif card == "A":
            return 14

    logger.info("should never reach here!")
    return 15


def is_greater(a, b):
    """return True if a > b, False otherwise

    Args:
        a (tuple): camel hand 1
        b (tuple): camel hand 2
    """
    if a["hand_type"] == b["hand_type"]:
        for i in range(len(a["cards"])):
            a_val = get_card_value(a["cards"][i])
            b_val = get_card_value(b["cards"][i])
            if a_val > b_val:
                return True
            elif a_val < b_val:
                return False
    else:
        return a["hand_type"] > b["hand_type"]

    # should never get here!
    logger.info("should not reach this point!")
    return False


def is_greater_2(a, b):
    """return True if a > b, False otherwise

    Args:
        a (tuple): camel hand 1
        b (tuple): camel hand 2
    """
    if a["hand_type"] == b["hand_type"]:
        for i in range(len(a["cards"])):
            a_val = get_card_value_2(a["cards"][i])
            b_val = get_card_value_2(b["cards"][i])
            if a_val > b_val:
                return True
            elif a_val < b_val:
                return False
    else:
        return a["hand_type"] > b["hand_type"]

    # should never get here!
    logger.info("should not reach this point!")
    return False


def get_total_winnings(data):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    hands = [
        {"cards": cards, "bid": bid, "hand_type": get_hand_type(cards)}
        for (cards, bid) in data
    ]

    sorted_hands = [hands[0]]
    for hand in hands[1:]:
        for i, h in enumerate(sorted_hands):
            # check if it should be inserted before the current hand
            if is_greater(h, hand):
                sorted_hands.insert(i, hand)
                break
            # if it's greater than the current hand and this is the last item, append
            elif (i + 1) == len(sorted_hands):
                sorted_hands.append(hand)
                break

    for i, hand in enumerate(sorted_hands):
        logger.debug(
            "hand: %s, bid: %s, rank: %d", "".join(hand["cards"]), hand["bid"], i + 1
        )

    winnings = sum([(i + 1) * hand["bid"] for i, hand in enumerate(sorted_hands)])
    return winnings


def get_total_winnings_2(data):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    hands = [
        {"cards": cards, "bid": bid, "hand_type": get_hand_type_2(cards)}
        for (cards, bid) in data
    ]

    sorted_hands = [hands[0]]
    for hand in hands[1:]:
        for i, h in enumerate(sorted_hands):
            # check if it should be inserted before the current hand
            if is_greater_2(h, hand):
                sorted_hands.insert(i, hand)
                break
            # if it's greater than the current hand and this is the last item, append
            if (i + 1) == len(sorted_hands):
                sorted_hands.append(hand)
                break

    for i, hand in enumerate(sorted_hands):
        logger.debug(
            "hand: %s, bid: %s, rank: %d", "".join(hand["cards"]), hand["bid"], i + 1
        )

    winnings = sum([(i + 1) * hand["bid"] for i, hand in enumerate(sorted_hands)])
    return winnings


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = get_total_winnings(data)
    print(f"Day 7: Part 1: Get Total Winnings (no jokers): {answer}")
    answer2 = get_total_winnings_2(data)
    print(f"Day 7: Part 2: Get Total Winnings (with jokers): {answer2}")


if __name__ == "__main__":
    main()
