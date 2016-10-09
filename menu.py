from colorama import Fore
from helper import *

allowed = ['1', '2', '3', 'q']


def menu_options():
    print("1: Python Info\n")
    print("2: System Info\n")
    print("3: CPU Info\n")
    print("q: quit menu.py\n")


def pretty_print(d):

    for key in d.keys():
        output = key + "\t" + d[key]
        print(output.expandtabs(30))


def main():
    menu_options()
    while(True):
        print("------------------------------------------\n")
        try:
            entry = str(
                input(
                    "Waehle " +
                    Fore.RED +
                    str(allowed) +
                    Fore.WHITE +
                    ": "))

            assert entry in allowed

            if entry == '1':
                print("Python Version: " + python_info())
            elif entry == '2':
                pretty_print(system_info())
            elif entry == '3':
                pass
            else:
                print("Programm beendet.")
                sys.exit()

        except ValueError:
            print("Menueoption existiert nicht. Erneut eineben.")

if __name__ == "__main__":
    main()
