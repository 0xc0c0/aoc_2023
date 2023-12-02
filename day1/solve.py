import logging
import os

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

def get_file_data(fn='input.txt'):
    with open(fn) as f:
        data = f.read()
    return data

def get_cal_val(text):
    logger.debug(text)
    digits = [x for x in text if x.isdigit()]
    val = int(f"{digits[0]}{digits[-1]}")
    return val

def get_cal_sum(calibration_lines):
    logger.debug(calibration_lines)
    return sum([get_cal_val(x) for x in calibration_lines])

def get_cal_val_part2(text):
    logger.debug(f"oldtext: {text}")
    digits = list()
    for i in range(len(text)):
        if text[i].isdigit():
            digits.append(text[i])
        elif text[i:].find('one') == 0:
            digits.append('1')
        elif text[i:].find('two') == 0:
            digits.append('2')
        elif text[i:].find('three') == 0:       
            digits.append('3')
        elif text[i:].find('four') == 0:
            digits.append('4')
        elif text[i:].find('five') == 0:
            digits.append('5')
        elif text[i:].find('six') == 0:
            digits.append('6')
        elif text[i:].find('seven') == 0:
            digits.append('7')
        elif text[i:].find('eight') == 0:
            digits.append('8')
        elif text[i:].find('nine') == 0:
            digits.append('9')
    logger.debug(digits)
    val = int(f"{digits[0]}{digits[-1]}")
    return val

def get_cal_sum_part2(calibration_lines):
    logger.debug(calibration_lines)
    return sum([get_cal_val_part2(x) for x in calibration_lines])

def parse_data(text_data):
    data = [line.strip() for line in text_data.strip().split('\n')]
    return data

def main():
    logger.setLevel(level=logging.INFO)
    data = get_file_data()
    calibration_lines = parse_data(data)
    answer = get_cal_sum(calibration_lines)
    print(f"Day 1: Calibration Sums (Part 1): {answer}")
    answer = get_cal_sum_part2(calibration_lines)
    print(f"Day 1: Calibration Sums (Part 2): {answer}")
    
if __name__ == '__main__':
    main()