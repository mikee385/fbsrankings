import os
import sys
sys.path.append(os.getcwd())

if "--use-typeguard" in sys.argv:
    print("Performing runtime type checks...")

    from typeguard.importhook import install_import_hook  # type: ignore
    with install_import_hook('fbsrankings'):
        import fbsrankings.main
else:
    import fbsrankings.main
