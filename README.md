# Simulatant

## Install requirements
Make sure you have node.js and Python (>= 3.8) installed. Then run:
```
npm install
(sudo) pip install -r requirements.txt
```

## Make virtual enviroment

Make environment
```
python -m venv venv
```
activiate it using activation scripts in venv/Scripts/ and then install requirements:

```
pip install -r requirements.txt
```
Optionally, deleted unused libraries in `venv\Lib\site-packages\torch\lib`.

### Create database
First time you run the code you need to populate the database:
```
python pysrc/db/manage.py migrate
```

### Run (development) as app
```
npm run serve
```

### Run (development) in webserver:
```
npm run webserve
python pysrc/simulserver.py
```

### Build app (production)
```
npm run build
```
To launch on Windows simply open
```
dist\win-unpacked\simultant.exe
```
On *nix you need to separately run
```
./dist/linux-unpacked/simultant
./dist/simulserver/simulserver
```
