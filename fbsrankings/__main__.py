from __future__ import absolute_import

import os
import sys

if sys.path[0] in ("", os.getcwd()):
    sys.path.pop(0)

package_dir = os.path.dirname(__file__)
os.chdir(package_dir)

project_dir = os.path.dirname(package_dir)
sys.path.insert(0, project_dir)

use_typeguard = False
if "--use-typeguard" in sys.argv:
    use_typeguard = True

if use_typeguard:
    print("Performing runtime type checks...")

    from typeguard.importhook import install_import_hook

    with install_import_hook("fbsrankings"):
        from fbsrankings.main import main
else:
    from fbsrankings.main import main

if __name__ == "__main__":
    sys.exit(main())
