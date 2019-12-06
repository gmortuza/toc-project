class TM:
    def __init__(self, file_in):
        self.states, self.symbols, self.transition, self.tape_content =self._read_file(file_in)
        pass

    def _read_file(self, file_in):
        # Make every thing string so that we don't need to conver back and forth
        with open(file_in, "r") as file:
            file_data = file.readlines()
            # The first line will be state.
            states = [str(i) for i in range(int(file_data[0].rstrip()))]
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
                    single_transition = transitions.pop(0).rstrip().replace(',','')
                    transition_details[state][symbol] = {}
                    transition_details[state][symbol]["next_state"] = single_transition[0]
                    transition_details[state][symbol]["write_symbol"] = single_transition[1]
                    transition_details[state][symbol]["move"] = single_transition[2]
            # The last line will be the initial tape status
            initial_tape_content = list(file_data[-1].rstrip())
        return states, symbols, transition_details, initial_tape_content


if __name__ == "__main__":
    tm = TM(file_in="BB31101.txt")
