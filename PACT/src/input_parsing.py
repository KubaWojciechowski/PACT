import argparse

def input_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", default='output',
                        help="Output directory path")
    parser.add_argument("-t", "--threshold", default=-
                        236, help="Energy threshold")
    args = parser.parse_args()

    return args

