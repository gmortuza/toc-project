import sys
from tm import TM


if __name__ == "__main__":
    tm = TM(sys.argv[1])
    tm.start_machine()
    tm.display_tape()