from cx_Freeze import setup, Executable

options = {"packages": ["os"]}

target = Executable(
    script="Octave.py",
    base="Win32GUI",
    icon="illu.ico"
    )

setup(
    name="Octave",
    version="1.0",
    description="Music Player",
    author="Manibharathi",
    options={"build_exe": options},
    executables=[target]
    )