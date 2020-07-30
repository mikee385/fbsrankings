import sys
from warnings import filterwarnings

from typeguard import TypeChecker, TypeWarning

from fbsrankings import cli


def main():
    use_typeguard = False
    if "--use-typeguard" in sys.argv:
        sys.argv.remove("--use-typeguard")
        use_typeguard = True

    if use_typeguard:
        print("Performing runtime type checks...")

        filterwarnings("always", category=TypeWarning)
        with TypeChecker(["fbsrankings"]):
            cli.main()
    else:
        cli.main()

if __name__ == "__main__":
    main()
