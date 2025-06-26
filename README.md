# Training eines Roboterarms über ein Neuronales Netzwerk

## Git Kurzanleitung:

Projekt kopieren:

```bash
git clone git@github.com:MKesenheimer/ai-reverse-kinematic.git
```

Änderungen von github holen und lokale Version updaten:

```bash
git pull
```

Gibt es lokale Änderungen zur aktuellen Version?

```bash
git diff
```

Lokale Änderungen zwischenspeichern:

```bash
git add --all
git commit -m "<Beschreibung der Änderungen>"
```

Lokale Änderungen auf github veröffentlichen:

```bash
git push
```


## Installation

Linux / Unix:

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m ensurepip --upgrade
pip3 install -r Requirements.txt
```

Windows:
```bash
python -m venv C:\Users\<username>\<projekt>\venv
cd C:\Users\<username>\<projekt>
venv\Scripts\activate.bat
python -m ensurepip --upgrade
pip install -r Requirements.txt
```

Siehe [Python venv](https://docs.python.org/3/library/venv.html) für weitere Information.

## Benutzung

Linux / Unix:

```bash
source venv/bin/activate
python simulation.py
```

Windows:

```bash
venv\Scripts\activate.bat
python simulation.py
```
