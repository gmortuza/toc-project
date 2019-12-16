import sys
from tm import TM


if __name__ == "__main__":
    try:
        tm = TM(sys.argv[1])
    except Exception as e:
        print("Input error. No file name was provided")
        sys.exit(0)
    tm.start_machine()
    tm.display_tape()