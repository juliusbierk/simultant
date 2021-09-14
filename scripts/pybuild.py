import os

if os.name == 'nt':
    os.system('venv/bin/pyinstaller --noconfirm simulserver.spec')
else:
    os.system('venv/bin/pyinstaller --noconfirm simulserver.spec')
