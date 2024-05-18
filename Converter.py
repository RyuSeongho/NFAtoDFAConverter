import FiniteAutomata
import os
import glob

def main():
    file_path = "C:\\Users\\ryuse\\Desktop\\류성호\\동국대학교\\3학년\\1학기\\형식언어\\HW2\\NFA"
    files = glob.glob(os.path.join(file_path, "*.txt"))

    for file in files:
        fa = FiniteAutomata.FiniteAutomata(file)
        print(os.path.basename(file))
        print(fa.__str__())
        print(fa.make_dfa().__str__())
        print('\n')


if __name__ == "__main__":
    main()
