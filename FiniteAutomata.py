# FiniteAutomata.py

from TextParser import parse_to_object


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

    # def epsilon_closure(self, states):
    #     # 입실론 클로저 계산 로직
    #     pass
    #
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
