class TM:
    def __init__(self, file_in):
        self.transitions, self.initial_tape, self.final_state = self._read_file(file_in)
        # This will contain the index of the tape head
        # The tape will be a python list
        self.current_tape_location = 0
        self.final_tape = None

    def start_machine(self):
        # Current state will always start from 0
        # tape will contains the initial tape value that is read from the input file
        # If the tape is empty there will be a list with one zero only
        # Tape head index will always start from zero
        self.final_tape = self.propagate_machine(current_state='0', tape=self.initial_tape, tape_head_index=0)

    def display_tape(self):
        print("".join(i for i in self.final_tape))

    def propagate_machine(self, current_state, tape, tape_head_index):
        while True:
            if current_state == self.final_state:
                return tape
            symbol = tape[tape_head_index]
            # get the transition for this current state and symbol
            transition = self.transitions[current_state][symbol]
            # Write in the tape
            tape[tape_head_index] = transition["write_symbol"]
            # Move tape head
            # if tape head is zero and we need to go left. Then we need to insert another zero at the beginning.
            # And keep the tape_head_index as 0
            if tape_head_index == 0 and transition["move"] == 'L':
                # Don't need to change the head position. It will still be 0
                tape.insert(0, '0')
            elif tape_head_index == len(tape) - 1 and transition["move"] == "R":
                tape.append('0')
                tape_head_index += 1
            elif transition["move"] == "R":
                tape_head_index += 1
            elif transition["move"] == "L":
                tape_head_index -= 1

            current_state = transition["next_state"]

    @staticmethod
    def _read_file(file_in):
        # Make every thing string so that we don't need to conver back and forth
        with open(file_in, "r") as file:
            file_data = file.readlines()
            # The first line will be state.
            states = [str(i) for i in range(int(file_data[0].rstrip()))]
            # The last state will be the final state
            final_state = states[-1]
            # The second line will be symbol. # it will include 0. that means it will have blank symbol inside it.
            # The tape symbols(gamma) and symbols(sigma) is same
            symbols = [str(i) for i in range(int(file_data[1].rstrip()) + 1)]
            # The rest of the line will be transition function
            # transitions = [list(single_transition.rstrip().replace(',','')) for single_transition in file_data[2:-1]]
            transitions = file_data[2:-1]
            transition_details = {}
            for state in states:
                if state == states[-1]:
                    break  # There won't by any transition from last one
                transition_details[state] = {}
                for symbol in symbols:
                    if len(transitions) <= 0:
                        break  # if somehow there is lack of transition we won't continue
                    single_transition = transitions.pop(0).rstrip().replace(',', '')
                    transition_details[state][symbol] = {}
                    transition_details[state][symbol]["next_state"] = single_transition[0]
                    transition_details[state][symbol]["write_symbol"] = single_transition[1]
                    transition_details[state][symbol]["move"] = single_transition[2]
            # The last line will be the initial tape status
            initial_tape_content = list(file_data[-1].rstrip())
            if len(initial_tape_content) == 0:
                initial_tape_content.append('0')
        return transition_details, initial_tape_content, final_state


# if __name__ == "__main__":
#     tm = TM(file_in="BB2.txt")
#     tm.start_machine()
#     tm.display_tape()
