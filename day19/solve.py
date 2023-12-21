#!/usr/bin/env python

"""Python solver file for Advent of Code Day 19"""
import os
import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)


def get_file_data(fn="input.txt"):
    """Function returning data blob from input.txt file"""
    with open(fn, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def parse_rule(text_rule):
    """Parse workflow rule

    Args:
        text_rule (_type_): _description_

    Returns:
        _type_: _description_
    """
    if ":" not in text_rule:
        return {"cat": None, "cmp_op": None, "value": None, "result": text_rule}

    text_logic, result = text_rule.strip().split(":")
    cat = text_logic[0]
    cmp_op = text_logic[1]
    value = int(text_logic[2:])
    return {"cat": cat, "cmp_op": cmp_op, "value": value, "result": result}


def parse_workflow(text_line):
    """Parses single line of text from the input file

    Args:
        text_line (str): raw text line from input file
    """
    rule, text_rules = text_line.strip().strip("}").split("{")
    rules = [parse_rule(r) for r in text_rules.strip().split(",")]
    return {rule: rules}


def parse_part_line(text_line):
    """Parses single line into a part rating object

    Args:
        text_line (_type_): _description_
    """
    text_ratings = text_line.strip("{").strip("}").split(",")
    ratings = {
        k: int(v) for text_entry in text_ratings for k, v in [text_entry.split("=")]
    }
    return ratings


def parse_data(text_data):
    """Parses full data input

    Args:
        text_data (str): raw text blob from input file

    Returns:
        _type_: parsed input data ready for processing
    """
    text_workflows, text_parts = text_data.strip().strip("\n").split("\n\n")
    workflows = {
        k: v
        for entry in text_workflows.strip().split("\n")
        for k, v in parse_workflow(entry).items()
    }
    parts = [parse_part_line(p) for p in text_parts.strip().split("\n")]
    return workflows, parts


def check_part(workflows, part, start="in"):
    cur = start
    while True:
        if cur == "A":
            return True
        if cur == "R":
            return False
        for rule in workflows[cur]:
            if rule["cmp_op"]:
                cat = rule["cat"]
                cmp_op = rule["cmp_op"]
                value = rule["value"]
                result = rule["result"]
                if cmp_op == "<":
                    if part[cat] < value:
                        cur = result
                        break
                if cmp_op == ">":
                    if part[cat] > value:
                        cur = result
                        break
            else:
                # jump to automatic next workflow
                cur = rule["result"]
                break

    logger.info("should never reach here")


def function(workflows, parts):
    """Complete Part 1 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 1 question
    """
    accepted_parts = [part for part in parts if check_part(workflows, part)]
    return sum([sum(part.values()) for part in accepted_parts])


def function2(workflows):
    """Complete Part 2 work

    Args:
        data (list): list of parsed input objects/dictionaries

    Returns:
        int: answer to Part 2 question
    """
    # get all distinct bifurcation values by cats, across all workflow rules
    dividers = {"x": {1, 4001}, "m": {1, 4001}, "a": {1, 4001}, "s": {1, 4001}}
    for workflow_rules in workflows.values():
        for rule in workflow_rules:
            cat = rule["cat"]
            if cat:
                # get the lowest integer value in the upper range
                if rule["cmp_op"] == "<":
                    dividers[cat].add(rule["value"])
                else:
                    dividers[cat].add(rule["value"] + 1)

    x_div = list(dividers["x"])
    x_div.sort()
    m_div = list(dividers["m"])
    m_div.sort()
    a_div = list(dividers["a"])
    a_div.sort()
    s_div = list(dividers["s"])
    s_div.sort()

    logger.debug(
        "total_to_check: %d",
        (len(x_div) - 1) * (len(m_div) - 1) * (len(a_div) - 1) * (len(s_div) - 1),
    )

    accepted_total = 0
    for i_x, x in enumerate(x_div[:-1]):
        for i_m, m in enumerate(m_div[:-1]):
            for i_a, a in enumerate(a_div[:-1]):
                for i_s, s in enumerate(s_div[:-1]):
                    if check_part(workflows, {"a": a, "m": m, "x": x, "s": s}):
                        # this subrange should then all be accepted
                        x_next = x_div[i_x + 1]
                        m_next = m_div[i_m + 1]
                        a_next = a_div[i_a + 1]
                        s_next = s_div[i_s + 1]
                        accepted = (
                            (x_next - x) * (m_next - m) * (a_next - a) * (s_next - s)
                        )
                        logger.debug(
                            "(%d, %d), (%d, %d), (%d, %d), (%d, %d): accepted: %d",
                            x,
                            x_next,
                            m,
                            m_next,
                            a,
                            a_next,
                            s,
                            s_next,
                            accepted,
                        )
                        accepted_total += accepted

    return accepted_total


def main():
    """Main function used to solve AoC problem"""
    logger.setLevel(level=logging.DEBUG)
    text_data = get_file_data()
    workflows, parts = parse_data(text_data)
    answer = function(workflows, parts)
    print(f"Day 19: Part 1: Get All Accepted Parts : {answer}")
    answer2 = function2(workflows)
    print(
        f"Day 19: Part 2: Get Total Distinct Combinations (1 Hour Runtime): {answer2}"
    )


if __name__ == "__main__":
    main()
