# TextPrinter.py
import os


def print_txt(fa, folder_name):
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)

    directory = current_directory + "/output"

    directory = os.path.join(directory, folder_name)

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, fa.file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"StateSet = {{{', '.join(sorted(fa.state_set))}}}\n")
        file.write(f"TerminalSet = {{{', '.join(sorted(fa.terminal_set))}}}\n")
        file.write("DeltaFunctions = {\n")
        for (from_state, terminal), to_state in fa.delta_functions.items():
            file.write(f"\t({from_state}, {terminal}) = {{{', '.join(sorted(to_state))}}}\n")
            """
            states = to_state.copy()

            to_state_print = str(states.pop())
            while states:
                state_element = states.pop()
                to_state_print += (', ' + state_element)
            file.write(f"\t({from_state}, {terminal}) = {to_state_print}\n")
            """
        file.write("}\n")
        file.write(f"StartState = {fa.start_state}\n")
        file.write(f"FinalStateSet = {{{', '.join(sorted(fa.final_state_set))}}}\n")