import os

if os.name == 'nt':
    os.system(r'venv\Scripts\python.exe pysrc/db/manage.py migrate')
    os.system(r'venv\Scripts\pyinstaller --noconfirm simulserver.spec')
else:
    os.system(r'venv/bin/python pysrc/db/manage.py migrate')
    os.system(r'venv/bin/pyinstaller --noconfirm simulserver.spec')
