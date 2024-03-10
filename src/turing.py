import json
import re


def machine(file_path, tape):
    config = get_json_data(file_path)
    return process_tape(config, tape)


def get_json_data(file_path):
    file = open(file_path, 'r')
    return json.load(file)


def process_tape(config, tape):
    state = config['initial']
    transitions = config['transitions']
    index = 3
    tape = re.sub(r'^\.+', '', tape)
    tape = re.sub(r'\.+$', '', tape)
    tape = "..." + tape + "..."
    state, tape = process_element(index, tape, state, transitions, config["finals"])
    return tape


def process_element(current_index, tape, current_state, transitions, final_states):
    if current_index >= len(tape):
        raise Exception("Instruction is wrong or input is wrong")
    try:
        instruction = list(filter(lambda x: x["read"] == tape[current_index], transitions[current_state]))
    except Exception as e:
        raise Exception("There is no instruction for {} in state {}".format(tape[current_index], current_state))
    if not instruction:
        raise Exception("There is no instruction for {} in state {}".format(tape[current_index], current_state))
    new_state = instruction[0]["to_state"]
    print_tape(tape, current_index, current_state, instruction)
    new_tape = tape[:current_index] + instruction[0]["write"] + tape[current_index+1:]
    if instruction[0]["action"] == "RIGHT":
        new_index = current_index + 1
    elif instruction[0]["action"] == "LEFT":
        new_index = current_index - 1
    else: raise Exception("Wrong action {}".format(instruction[0]["action"]))

    if new_state in final_states:
        print_final_tape(new_tape, new_index)
        return new_state, new_tape

    return process_element(new_index, new_tape, new_state, transitions, final_states)


def print_tape(tape, index, state, instruction):
    output_tape = ''.join(['<' + char + '>' if i == index else char for i, char in enumerate(tape)])
    print("[{}] ({}, {}) -> ({}, {}, {})".format(output_tape, state, instruction[0]["read"],
                                                 instruction[0]["to_state"], instruction[0]["write"],
                                                 instruction[0]["action"]))


def print_final_tape(tape, index):
    output_tape = ''.join(['<' + char + '>' if i == index else char for i, char in enumerate(tape)])
    print("[{}]".format(output_tape))
