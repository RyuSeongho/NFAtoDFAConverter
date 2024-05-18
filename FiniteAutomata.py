# FiniteAutomata.py

from TextParser import parse_to_object
from collections import deque
from EpsilonClosure import epsilon_closure as ec


class FiniteAutomata:
    def __init__(self, file_path=None):
        self.state_set = set()
        self.terminal_set = set()
        self.delta_functions = {}
        self.start_state = None
        self.final_state_set = set()

        if file_path:
            self.parse(file_path)

    def parse(self, file_path):
        (self.state_set,
         self.terminal_set,
         self.delta_functions,
         self.start_state,
         self.final_state_set) = parse_to_object(file_path)

    def __str__(self):
        return (f"StateSet={self.state_set}\n"
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
            result += ','

        result = result.rstrip(',')
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

        return result

    def make_dfa(self):

        dfa = FiniteAutomata()

        dfa.terminal_set.update(self.terminal_set)
        start_state_ep = ec(self, self.start_state)
        dfa.start_state = FiniteAutomata.integrate(start_state_ep)

        dfa.state_set.add(dfa.start_state)

        for final_state in self.final_state_set:
            if final_state in start_state_ep:
                dfa.final_state_set.add(dfa.start_state)

        task_state_set_queue = deque()
        task_state_set_queue.append(dfa.start_state)

        print("tssq:", task_state_set_queue)
        print(len(task_state_set_queue))

        while len(task_state_set_queue) > 0:
            curr_state_integrated = task_state_set_queue.popleft()
            print(len(task_state_set_queue))
            curr_state_set = curr_state_integrated.strip('[]').split(',')
            print("css", curr_state_set)

            for terminal in dfa.terminal_set:
                if terminal == 'ε':
                    continue

                result_set_for_terminal = set()
                for state in curr_state_set:
                    result_set = self.calc(state, terminal)
                    if len(result_set) <= 0:
                        continue
                    for result in result_set:
                        result_set_for_terminal.add(result)

                if len(result_set_for_terminal) <= 0:
                    continue

                integrated_string = FiniteAutomata.integrate(result_set_for_terminal)
                dfa.delta_functions[(curr_state_integrated, terminal)] = integrated_string

                print("result", terminal, integrated_string)

                if integrated_string in dfa.state_set:
                    continue

                task_state_set_queue.append(integrated_string)
                dfa.state_set.add(integrated_string)

                for final_state in self.final_state_set:
                    if final_state in result_set_for_terminal:
                        dfa.final_state_set.add(integrated_string)
                        break

        return dfa

    # def to_dfa(self):
    #     # (ε-)NFA를 DFA로 변환
    #     pass
    #
    # def minimize_dfa(self):
    #     # DFA 최소화
    #     pass
    #
    # def write_to_file(self, filename):
    #     with open(filename, 'w') as file:
    #         # 상태 기계 정보를 파일로 쓰는 로직 구현
    #         pass
