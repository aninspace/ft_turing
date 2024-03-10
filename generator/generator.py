import json


def main():
    data = {}
    data["name"] = "nested_unary_add"
    alphabet = ["!", "A", "B", "C", "D", "Z", "(", ")", "{", "}", "[", "]", ">", "<", ".", "1", "+", "=", "-", "*", "."]
    data["alphabet"] = alphabet
    data["blank"] = "."
    data["initial"] = "start"
    finals = ["HALT"]
    data["finals"] = finals

    get_states_and_transitions(alphabet, data)

    file_path = "data.json"
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def get_states_and_transitions(alphabet, data):
    new_states = []
    transitions = {}
    tape_states = ["A", "B", "C", "D", "Z"]
    new_states.append("start")
    new_states.append("HALT")
    new_states.append("Z_replace_symbol_to_*")
    start_transitions = []
    for state in tape_states:
        start_transitions.append({"read": state, "to_state": state + "_go_to_tape", "write": state, "action": "RIGHT"})
    transitions["start"] = start_transitions
    for state in tape_states:
        state_go_to_tape = state + "_go_to_tape"
        new_states.append(state_go_to_tape)
        new_transitions = fill_transitions_for_going_to_the_tape(alphabet, state_go_to_tape, state)
        transitions[state_go_to_tape] = new_transitions
        if state != "Z":
            state_replace_symbol = state + "_replace_symbol_to_*"
            new_states.append(state_replace_symbol)
            transitions[state_replace_symbol] = fill_transitions_for_replacing_symbol(state, new_states)
        fill_transitions_for_finding_the_begin(alphabet, state, transitions, new_states)
        fill_transitions_for_finding_the_state(alphabet, state, transitions, new_states)
        fill_transitions_for_finding_the_operation(alphabet, state, transitions, new_states)
        fill_transitions_for_finding_transition(alphabet, state, transitions, new_states)
        fill_transitions_for_finding_next_transition(alphabet, state, transitions, new_states)
    fill_transitions_for_getting_states(transitions, tape_states, new_states)
    fill_transitions_for_getting_writing_symbols(transitions, tape_states, new_states)
    fill_transitions_for_getting_directions(transitions, tape_states, new_states)
    fill_transitions_for_writing_symbols(transitions, tape_states, alphabet, new_states)
    fill_transitions_for_halt_state(transitions)

    seen = set()
    no_duplicate_states = [x for x in new_states if not (x in seen or seen.add(x))]
    data["states"] = no_duplicate_states
    data["transitions"] = transitions


def fill_transitions_for_halt_state(transitions):
    symbols = [".", "1", "+", "="]
    new_transitions = []
    for symbol in symbols:
        new_transitions.append({"read": symbol, "to_state": "HALT", "write": symbol, "action": "RIGHT"})
    transitions["Z_replace_symbol_to_*"] = new_transitions


def fill_transitions_for_going_to_the_tape(alphabet, state_name, state):
    new_transitions = []
    for letter in alphabet:
        if letter != "-":
            new_transitions.append({"read": letter, "to_state": state_name, "write": letter, "action": "RIGHT"})
    new_transitions.append({"read": "-", "to_state": state + "_replace_symbol_to_*", "write": "-", "action": "RIGHT"})
    return new_transitions


def fill_transitions_for_replacing_symbol(state, new_states):
    symbols = [".", "1", "+", "="]
    new_transitions = []
    for letter in symbols:
        new_states.append(state + "_begin_for_" + letter)
        new_transitions.append(
            {"read": letter, "to_state": state + "_begin_for_" + letter, "write": "*", "action": "LEFT"})
    return new_transitions


def fill_transitions_for_finding_the_begin(alphabet, state_name, transitions, new_states):
    symbols = [".", "1", "+", "="]
    for symbol in symbols:
        new_transitions = []
        transition_name = state_name + "_begin_for_" + symbol
        new_states.append(transition_name)
        for letter in alphabet:
            if letter != "!":
                new_transitions.append({"read": letter, "to_state": transition_name, "write": letter, "action": "LEFT"})
        new_states.append(state_name + "_find_state_" + symbol)
        new_transitions.append(
            {"read": "!", "to_state": state_name + "_find_state_" + symbol, "write": "!", "action": "RIGHT"})
        transitions[transition_name] = new_transitions


def fill_transitions_for_finding_the_state(alphabet, state_name, transitions, new_states):
    symbols = [".", "1", "+", "="]
    for symbol in symbols:
        new_transitions = []
        transition_name = state_name + "_find_state_" + symbol
        new_states.append(transition_name)
        for letter in alphabet:
            if letter != state_name:
                new_transitions.append({"read": letter, "to_state": transition_name, "write": letter, "action": "RIGHT"})
        new_states.append(state_name + "_find_operation_" + symbol)
        new_transitions.append(
            {"read": state_name, "to_state": state_name + "_find_operation_" + symbol, "write": state_name,
             "action": "RIGHT"})
        transitions[transition_name] = new_transitions


def fill_transitions_for_finding_the_operation(alphabet, state_name, transitions, new_states):
    symbols = [".", "1", "+", "="]
    for symbol in symbols:
        new_transitions = []
        transition_name = state_name + "_find_operation_" + symbol
        for letter in alphabet:
            if letter != "{":
                new_states.append(state_name + "_find_state_" + symbol)
                new_transitions.append(
                    {"read": letter, "to_state": state_name + "_find_state_" + symbol, "write": letter, "action": "RIGHT"})
        new_transitions.append(
            {"read": "{", "to_state": state_name + "_find_transition_" + symbol, "write": "{", "action": "RIGHT"})
        new_states.append(state_name + "_find_transition_" + symbol)
        transitions[transition_name] = new_transitions


def fill_transitions_for_finding_transition(alphabet, state_name, transitions, new_states):
    symbols = [".", "1", "+", "="]
    for symbol in symbols:
        new_transitions = []
        transition_name = state_name + "_find_transition_" + symbol
        for letter in alphabet:
            if letter != "[" and letter != symbol:
                new_states.append(state_name + "_find_next_transition_" + symbol)
                new_transitions.append(
                    {"read": letter, "to_state": state_name + "_find_next_transition_" + symbol, "write": letter,
                     "action": "RIGHT"})
        new_transitions.append({"read": "[", "to_state": transition_name, "write": "[", "action": "RIGHT"})
        new_transitions.append({"read": symbol, "to_state": "get_state_" + symbol, "write": symbol, "action": "RIGHT"})
        new_states.append(transition_name)
        new_states.append("get_state_" + symbol, )
        transitions[transition_name] = new_transitions


def fill_transitions_for_finding_next_transition(alphabet, state_name, transitions, new_states):
    symbols = [".", "1", "+", "="]
    for symbol in symbols:
        new_transitions = []
        transition_name = state_name + "_find_next_transition_" + symbol
        for letter in alphabet:
            if letter != "]":
                new_states.append(transition_name)
                new_transitions.append({"read": letter, "to_state": transition_name, "write": letter, "action": "RIGHT"})
        new_states.append(state_name + "_find_transition_" + symbol)
        new_transitions.append({"read": "]", "to_state": state_name + "_find_transition_" + symbol, "write": "]", "action": "RIGHT"})
        transitions[transition_name] = new_transitions


def fill_transitions_for_getting_states(transitions, states, new_states):
    symbols = [".", "1", "+", "="]
    for symbol in symbols:
        new_transitions = []
        transition_name = "get_state_" + symbol
        new_states.append(transition_name)
        for state in states:
            new_transitions.append(
                {"read": state, "to_state": "get_write_" + state, "write": state, "action": "RIGHT"})
            new_states.append("get_write_" + state)
        transitions[transition_name] = new_transitions


def fill_transitions_for_getting_directions(transitions, states, new_states):
    symbols = [".", "1", "+", "="]

    for state in states:
        for symbol in symbols:
            transition_name = "get_direction_" + state + "_" + symbol
            new_transitions = []
            new_transitions.append({"read": "<", "to_state": state + "_write_<" + symbol, "write": "<", "action": "RIGHT"})
            new_transitions.append({"read": ">", "to_state": state + "_write_>" + symbol, "write": ">", "action": "RIGHT"})
            transitions[transition_name] = new_transitions
            new_states.append(transition_name)

    # symbols = ["<", ">"]
    # for state in states:
    #     new_transitions.append({"read": symbol, "state": "get_write_" + state + "_" + symbol, "write": symbol, "action": "RIGHT"})
    #     new_states.append("get_write_" + state + "_" + symbol)
    # for state in states:
    #     new_transitions = []
    #     transition_name = "get_direction_" + state
    #     for symbol in symbols:
    #         new_transitions.append(
    #             {"read": symbol, "to_state": "get_write_" + state + "_" + symbol, "write": symbol, "action": "RIGHT"})
    #         new_states.append("get_write_" + state + "_" + symbol)
    #     transitions[transition_name] = new_transitions


def fill_transitions_for_getting_writing_symbols(transitions, states, new_states):
    symbols = [".", "1", "+", "="]
    for state in states:
        new_transitions = []
        transition_name = "get_write_" + state
        new_states.append(transition_name)
        for symbol in symbols:
            new_transitions.append(
                {"read": symbol, "to_state": "get_direction_" + state + "_" + symbol, "write": symbol, "action": "RIGHT"})
            new_states.append("get_direction_" + state + "_" + symbol)
        transitions[transition_name] = new_transitions


def fill_transitions_for_writing_symbols(transitions, states, alphabet, new_states):
    symbols = [".", "1", "+", "="]
    for state in states:
        for symbol in symbols:
            new_transitions = []
            transition_name = state + "_write_>" + symbol
            new_states.append(transition_name)
            for letter in alphabet:
                if letter != "*":
                    new_transitions.append(
                        {"read": letter, "to_state": transition_name, "write": letter, "action": "RIGHT"})
            new_transitions.append(
                {"read": "*", "to_state": state + "_replace_symbol_to_*", "write": symbol, "action": "RIGHT"})
            transitions[transition_name] = new_transitions

    for state in states:
        for symbol in symbols:
            new_transitions = []
            transition_name = state + "_write_<" + symbol
            new_states.append(transition_name)
            for letter in alphabet:
                if letter != "*":
                    new_transitions.append(
                        {"read": letter, "to_state": transition_name, "write": letter, "action": "RIGHT"})
            new_transitions.append(
                {"read": "*", "to_state": state + "_replace_symbol_to_*", "write": symbol, "action": "LEFT"})
            transitions[transition_name] = new_transitions


if __name__ == "__main__":
    main()
