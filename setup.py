from cx_Freeze import setup, Executable

base = None    

executables = [Executable("folding@SUSTech.py", base="Win32GUI", icon="icon.ico")]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "folding@SUSTech",
    options = options,
    version = "0.1.4",
    description = 'An easy way to make contribution.',
    executables = executables
)