from __future__ import absolute_import

import os
import sys

if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

project_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_dir)
os.chdir(os.path.join(project_dir, "fbsrankings"))

if "--use-typeguard" in sys.argv:
    print("Performing runtime type checks...")

    from typeguard.importhook import install_import_hook  # type: ignore

    with install_import_hook("fbsrankings"):
        from fbsrankings.main import main
else:
    from fbsrankings.main import main

if __name__ == "__main__":
    sys.exit(main())
