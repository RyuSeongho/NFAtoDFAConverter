# FiniteAutomata.py

from TextParser import parse_to_object
from collections import deque
from EpsilonClosure import epsilon_closure as ec
import NamingModule as Settings


class FiniteAutomata:
    def __init__(self, file_path=None):
        self.state_set = set()
        self.terminal_set = set()
        self.delta_functions = {}
        self.start_state = None
        self.final_state_set = set()
        self.file_name = "UnnamedAutomata.txt"

        if file_path:
            self.parse(file_path)

    def parse(self, file_path):
        (self.state_set,
         self.terminal_set,
         self.delta_functions,
         self.start_state,
         self.final_state_set,
         self.file_name) = parse_to_object(file_path)

    def __str__(self):
        return (f"FileName={self.file_name}\n"
                f"StateSet={self.state_set}\n"
                f"TerminalSet={self.terminal_set}\n"
                f"DeltaFunctions={self.delta_functions}\n"
                f"StartState={self.start_state}\n"
                f"FinalStateSet={self.final_state_set}")

    @staticmethod
    def integrate(material_set):
        sorted_list = sorted(list(material_set))
        result = '['
        for material in sorted_list:
            result += str(material)
            result += ' '

        result = result.rstrip(' ')
        result += ']'

        return result

    def calc(self, start_state, terminal):
        result = set()

        key = (start_state, terminal)
        value = self.delta_functions.get(key)
        if value is not None:
            for single_value in value:
                value_ep = ec(self, single_value)
                for value_ep_single in value_ep:
                    result.add(value_ep_single)

        return sorted(list(result))

    def make_dfa(self):

        dfa = FiniteAutomata()

        dfa.file_name = self.file_name

        dfa.terminal_set.update(self.terminal_set)
        start_state_ep = ec(self, self.start_state)
        dfa.start_state = FiniteAutomata.integrate(start_state_ep)

        dfa.state_set.add(dfa.start_state)

        for final_state in self.final_state_set:
            if final_state in start_state_ep:
                dfa.final_state_set.add(dfa.start_state)

        task_state_set_queue = deque()
        task_state_set_queue.append(dfa.start_state)

        while len(task_state_set_queue) > 0:
            curr_state_integrated = task_state_set_queue.popleft()
            curr_state_set = curr_state_integrated.strip('[]').split(' ')

            for terminal in dfa.terminal_set:

                result_set_for_terminal = set()
                for state in curr_state_set:
                    result_list = self.calc(state, terminal)
                    if len(result_list) <= 0:
                        continue
                    for result in result_list:
                        result_set_for_terminal.add(result)

                if len(result_set_for_terminal) <= 0:
                    continue

                integrated_string = FiniteAutomata.integrate(result_set_for_terminal)
                dfa.delta_functions[(curr_state_integrated, terminal)] = {integrated_string}

                if integrated_string in dfa.state_set:
                    continue

                task_state_set_queue.append(integrated_string)
                dfa.state_set.add(integrated_string)

                for final_state in self.final_state_set:
                    if final_state in result_set_for_terminal:
                        dfa.final_state_set.add(integrated_string)
                        break

        return dfa

    def reduce_dfa(self):

        rdfa = FiniteAutomata()

        group = {}
        group_result_tuples = []
        prev_state_size = 2

        for state in self.state_set:
            if state in self.final_state_set:
                group[state] = 1
            else:
                group[state] = 0

        while True:
            new_group = {}
            for state in self.state_set:
                group_for_all_terminal = []
                curr_dict = {'group': group[state]}

                for terminal in sorted(self.terminal_set):
                    result_list = self.calc(state, terminal)
                    if len(result_list) <= 0:
                        group_for_all_terminal.append(-1)
                    else:
                        result = result_list.pop(0)
                        group_for_all_terminal.append(group[result])

                curr_dict['result'] = tuple(group_for_all_terminal)

                curr_tuple = tuple(curr_dict.items())

                if curr_tuple not in group_result_tuples:
                    group_result_tuples.append(curr_tuple)
                    new_group[state] = len(group_result_tuples) - 1
                else:
                    new_group[state] = group_result_tuples.index(curr_tuple)

            if prev_state_size == len(group_result_tuples):
                break

            group = new_group.copy()
            prev_state_size = len(group_result_tuples)
            group_result_tuples.clear()

        rdfa.file_name = self.file_name
        rdfa.terminal_set = self.terminal_set

        map_new_state_to_name = {}

        for i in range(prev_state_size):
            map_new_state_to_name[i] = '['

        for state in self.state_set:
            map_new_state_to_name[group[state]] += (str(state) + ' ')

        for item in map_new_state_to_name.items():
            map_new_state_to_name[item[0]] = item[1].rstrip(' ') + ']'

        for state in self.state_set:
            new_name = map_new_state_to_name[group[state]]
            rdfa.state_set.add(new_name)
            if state in self.final_state_set:
                rdfa.final_state_set.add(new_name)
            if state == self.start_state:
                rdfa.start_state = new_name

        for (state, terminal), value in self.delta_functions.items():

            new_key = (map_new_state_to_name[group[state]], terminal)
            new_value = map_new_state_to_name[group[value.pop()]]
            rdfa.delta_functions[new_key] = {new_value}

        return rdfa

    def convert_state_name(self, print_type='default'):
        if print_type == 'original':
            return self

        naming_module = Settings.NamingModule(print_type)
        new_fa = FiniteAutomata()
        new_fa.file_name = self.file_name
        new_fa.terminal_set = self.terminal_set

        map_new_state_to_name = {}

        state_list = sorted(list(self.state_set))

        for state in state_list:
            new_name = naming_module.get_name()
            map_new_state_to_name[state] = new_name
            new_fa.state_set.add(new_name)

            if state == self.start_state:
                new_fa.start_state = new_name

            if state in self.final_state_set:
                new_fa.final_state_set.add(new_name)

        for (state, terminal), value in self.delta_functions.items():
            new_key = (map_new_state_to_name[state], terminal)
            new_value_set = set()
            value_list = sorted(list(value))
            while value_list:
                new_value_set.add(map_new_state_to_name[value_list.pop(0)])
            new_fa.delta_functions[new_key] = new_value_set

        return new_fa
