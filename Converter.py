import FiniteAutomata
import os
import glob
from TextPrinter import print_txt
import argparse


def main():
    parser = argparse.ArgumentParser(description='Please specify the print type.')
    parser.add_argument('--nfa', type=str, help='nfa print type')
    parser.add_argument('--dfa', type=str, help='dfa print type')
    parser.add_argument('--reduced_dfa', type=str, help='reduced dfa print type')
    args = parser.parse_args()

    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    file_path = current_directory + "/input"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        print("no directory found ", file_path)
        return

    files = glob.glob(os.path.join(file_path, "*.txt"))

    if not files:
        print("no files found")
        return

    for file in files:
        fa = FiniteAutomata.FiniteAutomata(file)
        fa = fa.convert_state_name(args.nfa)
        print_txt(fa, "NFA")
        fa = fa.make_dfa()
        fa = fa.convert_state_name(args.dfa)
        print_txt(fa, "DFA")
        fa = fa.reduce_dfa()
        fa = fa.convert_state_name(args.reduced_dfa)
        print_txt(fa, "reduced DFA")

    print('Convert.. Reduce.. Tada!')


if __name__ == "__main__":
    main()
