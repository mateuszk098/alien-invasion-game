"""
This script creates a standalone executable file to run the gameas a .exe file 
without Python usage. 

To create executable file run the following command in the `code` directory:
python setup.py build -b ../build/

It creates a `build` directory in which you can find `main.exe` file.
"""

import sys
import subprocess
from cx_Freeze import setup
from cx_Freeze import Executable


def main():
    # sys.setrecursionlimit(5000)

    # Define the files and libraries you work with.
    """
    The first element in the tuple is a path to the files used by the .py files.
    By default, the setup script places the `assets` and `sounds` directories 
    alongside the .exe file. This will not work because the game code is not 
    alongside the `assets` and `sounds`. Therefore, one has to define new 
    relative paths. This way, the setup places these directories one level 
    higher than .exe.
    """
    include_files = {
        ("../assets/", "../assets/"),
        ("../sounds/", "../sounds/"),
    }
    packages = {
        "pygame",
    }

    # Save all installed libraries to exclude unnecessary ones while creating the executable file.
    installed_packages = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
    installed_packages_lst = installed_packages.decode("utf-8").split("\r\n")
    # All libraries are in the form of a list with only their names (without a version).
    excludes = {pkg.split("==")[0] for pkg in installed_packages_lst if pkg != ""}
    # Consider only unnecessary libraries.
    excludes = packages.symmetric_difference(excludes)

    build_exe_options = {
        "excludes": excludes,
        "packages": packages,
        "include_files": include_files,
        "optimize": 2,
        "silent": True,
    }

    bdist_msi_options = {
        # Place possible options here.
    }

    base = None
    if sys.platform == "win32":
        base = "Win32GUI"

    setup(
        name="Alien Invasion",
        version="1.0.0",
        description="Alien Invasion Game",
        author="MK",
        author_email="xxx@yyy.com",
        options={
            "build_exe": build_exe_options,
            "bdist_msi": bdist_msi_options,
        },
        executables=[Executable("main.py", base=base)]
    )


if __name__ == "__main__":
    main()
