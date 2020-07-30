import sys

use_typeguard = False
if "--use-typeguard" in sys.argv:
    sys.argv.remove("--use-typeguard")
    use_typeguard = True

if use_typeguard:
    print("Performing runtime type checks...")

    from typeguard.importhook import install_import_hook

    with install_import_hook("fbsrankings"):
        from fbsrankings.cli import main
else:
    from fbsrankings.cli import main

if __name__ == "__main__":
    main()
