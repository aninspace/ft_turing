import re
import sys
from functools import partial
import json


def validate(file_path, input):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
        return False
    return validate_file(data) and validate_input(input, data)


def validate_input(input, json_data):
    alphabet = json_data["alphabet"]
    blank = json_data["blank"]
    check_alphabet = alphabet
    check_alphabet.remove(blank)
    pattern = "[" + re.escape("".join(alphabet)) + "]+"
    input = re.sub(r'^\.+', '', input)
    input = re.sub(r'\.+$', '', input)
    if len(input) == 0:
        print("Input is empty")
        return False
    if bool(re.fullmatch(pattern, input)):
        return True
    else:
        print(f"Invalid input: {input} contains invalid characters")
        return False



def check_required_fields(state, transition, transitions):
    required_fields = {"read", "to_state", "write", "action"}
    transition_fields_set = set(transition.keys())
    return required_fields.issubset(
        transition_fields_set), f"Missing required fields in transition for state '{state}': {required_fields - transition_fields_set}"


def validate_transitions_helper(states, transitions, check_partial):
    if not states:
        return True
    else:
        state = states[0]
        transitions_list = transitions[state]
        transitions_pairs = [{"state": state, "transition": transition} for transition in transitions_list]
        are_all_valid = all(map(lambda pair: check_partial(**pair), transitions_pairs))

        return are_all_valid and validate_transitions_helper(states[1:], transitions, check_partial)


def validate_state_in_transition(state):
    required_fields = {"read", "to_state", "write", "action"}
    if not set(state.keys()) == required_fields:
        print(f"Missing required fields in transition for state '{state}")
    return set(state.keys()) == required_fields


def validate_states_in_transition(states_in_transitions):
    return all(validate_state_in_transition(state) for state in states_in_transitions)


def validate_transitions(data):
    alphabet = data.get("alphabet")
    transitions = data.get("transitions", {})
    check_partial = partial(check_required_fields, transitions=transitions)
    states = list(transitions.keys())
    states_in_json = data.get("states", {})
    states_in_json.remove("HALT")
    if not all(state in states_in_json for state in states):
        print("Missing required fields in states")
        return False
    are_all_valid = validate_transitions_helper(states, transitions, check_partial)
    if not are_all_valid:
        print("Validation errors:")
        return False

    keys = transitions.keys()
    states_in_json.append("HALT")
    is_valid = all(validate_states_in_transition(transitions[k]) for k in keys)
    is_valid_states = lambda d: all(d[key] != "" for key in d) and \
                         d.get('action') in ['RIGHT', 'LEFT'] and \
                         d.get('read', '') in alphabet and \
                         d.get('write', '') in alphabet and \
                         d.get('to_state') in states_in_json
    are_all_dicts_valid = lambda lst: all(map(is_valid_states, lst))
    are_all_transitions_valid = all(map(are_all_dicts_valid, transitions.values()))
    if not are_all_transitions_valid:
        print("Transitions are wrong")
        return False
    if not is_valid:
        print("Not all the steps into the states")
    return are_all_valid and is_valid


def validate_file(json_data):
    keys = ["name", "alphabet", "blank", "states", "initial", "finals", "transitions"]
    if not all(map(lambda key: key in json_data, keys)):
        print("Json does not contain all required keys")
        return False

    if not (isinstance(json_data.get("alphabet"), list) and all(
            isinstance(char, str) and len(char) == 1 for char in json_data["alphabet"])):
        print("Alphabet must contains only letters")
        return False
    if json_data.get("blank") not in json_data["alphabet"]:
        print("Blank char not in alphabet")
        return False
    if not (isinstance(json_data.get("states"), list) and all(isinstance(state, str) for state in json_data["states"])):
        print("States must contains only strings")
        return False
    if json_data.get("initial") not in json_data["states"]:
        print("Initial state not into states")
        return False
    if not all(final_state in json_data["states"] for final_state in json_data["finals"]):
        print("Error: Some states in 'finals' are not found in 'states'.")
        return False

    sys.setrecursionlimit(1000000)
    states_set = set(json_data["states"])
    finals_set = set(json_data["finals"])
    transitions_states_set = set(json_data["transitions"].keys())
    missing_states = states_set - finals_set - transitions_states_set


    if missing_states:
        print(f"Error: Some states in 'states' are missing in 'transitions': {missing_states}")
        return False

    return validate_transitions(json_data)
