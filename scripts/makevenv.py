import os

os.system('python -m venv venv')
if os.name == 'nt':
    os.system(r'venv\Scripts\pip.exe install -r requirements.txt')
else:
    os.system(r'venv/bin/pip install -r requirements.txt')
