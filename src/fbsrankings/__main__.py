import sys

USE_TYPEGUARD = False
if "--use-typeguard" in sys.argv:
    sys.argv.remove("--use-typeguard")
    USE_TYPEGUARD = True

if USE_TYPEGUARD:
    print("Performing runtime type checks...")

    from typeguard.importhook import install_import_hook

    with install_import_hook("fbsrankings"):
        from fbsrankings.cli import main
else:
    from fbsrankings.cli import main

if __name__ == "__main__":
    main()
