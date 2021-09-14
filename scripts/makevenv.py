import os

os.system('python -m venv venv')
if os.name == 'nt':
    os.system('venv/bin/pip.exe install -r requirements.txt')
else:
    os.system('venv/bin/pip install -r requirements.txt')
