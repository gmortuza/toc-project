"""
TODO: about project
"""
import copy
import sys
import logging

MAXIMUM_NUMBER_OF_TRANSITION = 100
found = False
language_dict = {}

def is_terminal(symbol):
    """
    Check if a symbol is terminal or a variable
    :param symbol: variable or terminal
    :return: True if terminal False otherwise
    """
    if symbol == "!" or symbol == "_":
        return True
    return not symbol.isupper()


def format_language(language):
    """
    Store the language in a dictionary so that it can be used properly
    It will create a dictionary of the language. Dictionary will contains a variable name as a key and a list as a value.
    The list will contain all the possible expression that the variable can replace.

    :param language: List of a language. Each list items will be an expression. Variable to expression will be seperated by ->
    """
    global language_dict  # The language will be used by all recursive function. So we make it global
    language = list(map(lambda x: x.split("->"), language))  # Split the language by "->"
    language_dict_unsorted = {}
    for single_rule in language:
        language_dict_unsorted.setdefault(single_rule[0], []).append(single_rule[1])  # Store expression of the variable as list item
    # We want to process the smallest expression of a variable first. It takes less time to process small one. If we are lucky that small one might be an accepted string so we don't need to calculate further.
    for key, value in language_dict_unsorted.items():
        language_dict[key] = sorted(value)


def read_file(file_in):
    # Read file
    try:
        with open(file_in, "r") as file:
            lines = file.readlines()
            #  Separating rules
            rules = list(map(lambda x: x.strip(), lines[1:int(lines[0]) + 1]))
            format_language(rules)
            # Separating input string
            input_string = list(map(lambda x: x.strip(), lines[int(lines[0]) + 1:]))
            # This is start variable. Dictionary might change the order so we store the start variable
            return input_string, rules[0][0]
    except:
        logging.error("File not found")
        exit()


def formulate_stack(single_expression, previous_stack):
    """
    If some terminal stay together we will consider the group of terminal as a single terminal.
    So that we can concatenate the terminal with process input in a single recursive function.
    That will save some recursive function
    :param single_expression: Expression that will be pushed into stack
    :param previous_stack: If there is already a stack we will push the expression into that
    :return:
    """
    if single_expression.islower() or single_expression == "!":
        # all lower case
        stack = [single_expression]
    else:
        start = 0
        stack = []
        for i, l in enumerate(single_expression):
            if l.isupper():
                stack.extend([single_expression[start: i], l])
                start = i + 1
        stack.extend(single_expression[start:])
    if previous_stack:
        stack.extend(previous_stack)
    return stack


def propagate(stack, concat, transition, input_string):
    """

    :param stack: Current stack condition.
    :param concat: Processed input string
    :param transition: Keep track of the number of transition
    :param input_string: original input string to cherck if that was accepted or not
    :return:
    """
    # found is checked by other recursive function if found is set true in one recursive function
    # all other recursive function will return
    global found
    if found or transition >= MAXIMUM_NUMBER_OF_TRANSITION or not stack:
        return
    if is_terminal(stack[0]):  # The first element of the stack is a terminal so we will append it with our process input string
        concat += stack.pop(0)
        # If the processed input string that is calculated so far isn't matched with input string then it will return
        # Cause there is no chance it will match in future.
        if concat.replace("!", "") != input_string[:len(concat.replace("!", ""))]:
            return
        # If process input is equal input string then we will set found=True and stop all other recursive function
        if concat.replace("!", "") == input_string:
            found = True
            return
        # After poping the the first element of stack. we get a new stack. First element of that stack might
        # be a terminal or variable. As we don't know that yet. We will just pass the new stack in the propagate
        # As we didn't replace any variable of the stack our transition didn't incremented
        propagate(stack=stack, concat=concat, transition=transition, input_string=input_string)
    else:  # we get a variable so we will do the propagation again
        for single_expression in language_dict[stack.pop(0)]:  # A single variable might have multiple expression we will check all expression
            new_stack = formulate_stack(single_expression, stack)
            # Concat was passing as a references so all the recursive function was getting the same concat.
            # So we created a deepcopy of the concat and pass that. so that every different stack has different concat
            copy_concat = copy.deepcopy(concat)
            propagate(stack=new_stack, concat=copy_concat, transition=transition+1, input_string=input_string)


def main():
    # read the file
    try:
        input_strings, start_variable = read_file(file_in=sys.argv[1])
    except:
        logging.error("A file is required as a command line argument")
        exit()
    for single_input_string in input_strings:  # We will check for each input string
        # If a single propagate find a match then that propagate method will set the found as True so by matching
        # that we can terminate all the propagate method
        global found
        found = False
        # The staring variable might have multiple expression
        for single_expression in language_dict[start_variable]:
            # each input will have a unique stack
            stack = formulate_stack(single_expression, False)
            propagate(stack=stack, concat="", transition=0, input_string=single_input_string.replace("!", ""))

        if found:
            print("yes")
        else:
            print("no")


if __name__ == '__main__':
    main()
