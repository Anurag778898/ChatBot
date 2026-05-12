# run_once_setup.py  ← Run this file ONCE to set up auto-start
import os
import sys

# Path to your main.py
script_path = os.path.abspath("main.py")
python_path = sys.executable

# Create a .bat file in Windows Startup folder
startup_folder = os.path.expandvars(
    r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
)

bat_content = f'@echo off\n"{python_path}" "{script_path}"\n'
bat_path = os.path.join(startup_folder, "jarvis.bat")

with open(bat_path, "w") as f:
    f.write(bat_content)

print(f"✅ JARVIS will now start automatically with Windows!")
print(f"   Startup file created at: {bat_path}")