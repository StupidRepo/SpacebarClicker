import cx_Freeze

executables = [ cx_Freeze.Executable("main.py") ]
with open("version.txt", "r") as versionFile:
    version = versionFile.read()
    versionFile.close()

cx_Freeze.setup(
    name = "Spacebar Clicker",
    options = {
        "build_exe": {
            "packages": ["pygame", "json", "sys", "appdirs"],
            "include_files": ["assets", "README.md", "LICENSE.md", "version.txt"]
        }
    },
    executables = executables,
    version = version
)