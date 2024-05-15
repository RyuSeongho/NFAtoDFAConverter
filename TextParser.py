# TextParser.py

import re


def parse_to_object(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().replace(' ', '').replace('\t', '')

        # Extracting different parts using regular expressions
        state_set_match = re.search(r'StateSet=\{([^}]*)\}\n', content)
        terminal_set_match = re.search(r'TerminalSet=\{([^}]*)\}\n', content)
        delta_functions_match = re.search(r'DeltaFunctions=([\s\S]*?)StartState=', content)
        start_state_match = re.search(r'StartState=([^,}]*)\n', content)
        final_state_set_match = re.search(r'FinalStateSet=\{([^}]*)}', content)

        state_set = set()
        terminal_set = set()
        delta_functions = {}
        start_state = None
        final_state_set = set()

        if state_set_match:
            states = state_set_match.group(1).split(',')
            state_set = set(states)
        if terminal_set_match:
            terminals = terminal_set_match.group(1).split(',')
            terminal_set = set(terminals)
        if delta_functions_match:
            transitions = delta_functions_match.group(1).strip('{}').split('\n')

            for transition in transitions:
                if transition:
                    if '=' not in transition:
                        continue

                    state_pair, to_states = transition.split('=')
                    state_pair = state_pair.strip('()').split(',')
                    from_state = state_pair[0]
                    symbol = state_pair[1]
                    to_states = to_states.strip('{}').split(',')
                    if (from_state, symbol) not in delta_functions:
                        delta_functions[(from_state, symbol)] = set(to_states)
                    else:
                        delta_functions[(from_state, symbol)].update(to_states)

        if start_state_match:
            start_state = start_state_match.group(1)
        if final_state_set_match:
            final_states = final_state_set_match.group(1).split(',')
            final_state_set = set(final_states)

        return state_set, terminal_set, delta_functions, start_state, final_state_set
