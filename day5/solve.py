#!/usr/bin/env python

"""Python solver file for Advent of Code Day 5"""
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
    return list(text_line)


def parse_stanza(text_stanza):
    """parse a stanza blob

    Args:
        text_stanza (_type_): _description_

    Returns:
        _type_: _description_
    """
    # logger.debug("text_stanza is %s", text_stanza)
    text_lines = text_stanza.split("\n")[1:]
    # logger.debug(text_lines)
    src_dst_sets = [[int(x) for x in line.strip().split()] for line in text_lines]
    return src_dst_sets


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    (
        text_seeds,
        text_seed_soil,
        text_soil_fertilizer,
        text_fertilizer_water,
        text_water_light,
        text_light_temp,
        text_temp_humid,
        text_humid_loc,
    ) = (
        text_data.strip().strip("\n").strip().split("\n\n")
    )
    seeds = [int(x) for x in text_seeds.split(":")[1].strip().split()]
    seed_soil = parse_stanza(text_seed_soil)
    soil_fertilizer = parse_stanza(text_soil_fertilizer)
    fertilizer_water = parse_stanza(text_fertilizer_water)
    water_light = parse_stanza(text_water_light)
    light_temp = parse_stanza(text_light_temp)
    temp_humid = parse_stanza(text_temp_humid)
    humid_loc = parse_stanza(text_humid_loc)

    mappings = (
        seed_soil,
        soil_fertilizer,
        fertilizer_water,
        water_light,
        light_temp,
        temp_humid,
        humid_loc,
    )

    return seeds, mappings


def find_lowest_location(seeds, mappings):
    """Complete Part 1 work

    Args:
        seeds (list) : list of ints representing seeds
        mappings (tuple) : tuple of lookup mappings with each entry inside mappings with
            pattern (dst_start, src_start, range)

    Returns:
        int: answer to Part 1 question
    """
    lowest_location = None
    for s in seeds:
        src = s
        for m in mappings:
            dst = src  # if nothing else found, it's a 1:1 mapping
            for dst_start, src_start, rng in m:
                if src_start <= src < (src_start + rng):
                    # found the offset
                    dst = (src - src_start) + dst_start
                    break
            src = dst
        if not lowest_location or src < lowest_location:
            lowest_location = src
    return lowest_location


def function2(seeds, mappings):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    seed_ranges = [(seeds[x], seeds[x + 1]) for x in list(range(0, len(seeds), 2))]
    src_ranges_to_process = seed_ranges
    for mapping in mappings:
        dst_ranges = list()
        while src_ranges_to_process:
            sr = src_ranges_to_process.pop()
            src_start, src_rng = sr
            src_end = src_start + src_rng

            # look for full or partial overlaps in mapping
            found_match = False
            for dst_start, map_src_start, rng in mapping:
                map_src_end = map_src_start + rng
                if src_start < map_src_start:
                    # case with partial/exact overlap with mapping, non-encompassing
                    if map_src_start < src_end <= map_src_end:
                        # non-overlapping portion gets re-added to "to_process" queue
                        src_ranges_to_process.append(
                            (src_start, map_src_start - src_start)
                        )

                        # overlapping portion continues to be processed
                        overlap_rng = src_end - map_src_start
                        dst_ranges.append((dst_start, overlap_rng))
                        found_match = True
                        break

                    # case where src is encompassing the entire range
                    elif src_end > map_src_end:
                        # non-overlapping portion 1
                        src_ranges_to_process.append(
                            (src_start, map_src_start - src_start)
                        )
                        # non-overlapping portion 2
                        src_ranges_to_process.append(
                            (map_src_end, src_end - map_src_end)
                        )
                        # overlapping portion gets processed
                        dst_ranges.append((dst_start, rng))
                        found_match = True
                        break

                    # irrelevant but here for completeness
                    elif src_end <= map_src_start:
                        continue

                elif map_src_start <= src_start < map_src_end:
                    # case with mapping encompassing src
                    if src_end <= map_src_end:
                        offset = src_start - map_src_start
                        dst_ranges.append((dst_start + offset, src_rng))
                        found_match = True
                        break

                    # case with partial overlap
                    elif map_src_end < src_end:
                        # non-overlapping portion
                        src_ranges_to_process.append(
                            (map_src_end, src_end - map_src_end)
                        )
                        # overlapping portion
                        offset_start = src_start - map_src_start
                        dst_ranges.append(
                            (dst_start + offset_start, map_src_end - src_start)
                        )
                        found_match = True
                        break

                # irrelevant but here for completeness
                elif src_start >= map_src_end:
                    continue

            if found_match is False:
                # maps 1:1 when there is no mapping
                dst_ranges.append(sr)
        # when complete, the dst_ranges become the next round's src_ranges
        src_ranges_to_process = dst_ranges

        # find lowest in all ranges as answer
        lowest_location = src_ranges_to_process[0][0]
        for start, _ in src_ranges_to_process:
            if start < lowest_location:
                lowest_location = start

    return lowest_location


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.INFO)
    text_data = get_file_data()
    data = parse_data(text_data)
    answer = find_lowest_location(*data)
    print(f"Day 5: Part 1: Find Lowest Value Location with Seed Inputs: {answer}")
    answer2 = function2(*data)
    print(
        f"Day 5: Part 2: Find Lowest Value Location with Seed Range Inputs: {answer2}"
    )


if __name__ == "__main__":
    main()
