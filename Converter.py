import FiniteAutomata
import os
import glob
from TextPrinter import print_txt

def main():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    file_path = current_directory + "/input"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        print("no directory found")
        return

    files = glob.glob(os.path.join(file_path, "*.txt"))

    if not files:
        print("no files found")
        return

    for file in files:

        fa = FiniteAutomata.FiniteAutomata(file)
        print(fa.__str__())
        print_txt(fa, "NFA")
        fa = fa.make_dfa()
        fa = fa.convert_state_name()
        print_txt(fa, "DFA")
        fa = fa.reduce_dfa()
        fa = fa.convert_state_name()
        print_txt(fa, "reduced DFA")
        print('\n')


if __name__ == "__main__":
    main()
