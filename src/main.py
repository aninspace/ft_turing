import argparse

from turing import machine
from validation import validate


def main():
    parser = argparse.ArgumentParser(description="Turing machine")
    parser.add_argument("jsonfile", help="JSON description of the machine")
    parser.add_argument("input", help="Input of the machine")


    args = parser.parse_args()
    if not validate(args.jsonfile, args.input):
        print("Validation failed")
        return
    try :
        machine(args.jsonfile, args.input)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
