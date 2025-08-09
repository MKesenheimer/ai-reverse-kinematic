# Training eines Roboterarms über ein Neuronales Netzwerk

## Git Kurzanleitung

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

Änderungshistorie anschauen ("commit log"):

```bash
git log
```

Lokale Änderungen auf letzten Commit zurücksetzen. Achtung! Dabei gehen die lokalen Änderungen verloren:

```bash
git reset --hard HEAD
```

Lokale Änderungen auf einen bestimmten Punkt zurücksetzen. Achtung! Dabei gehen die lokalen Änderungen verloren:

```bash
git reset --hard <commit-hash>
```

## Installation

Linux / Unix:

```bash
yay -S python311
```

```bash
cd ai-reverse-kinematic
python3.11 -m venv venv
source venv/bin/activate
python -m ensurepip --upgrade
pip3 install -r requirements.txt
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate.bat
python -m ensurepip --upgrade
pip install -r requirements.txt
```

Siehe [Python venv](https://docs.python.org/3/library/venv.html) für weitere Information.

### Redis server installieren und ausführen

Die Skripte `simulation.py` und `renderer.py` kommunizieren über einen Redis-Server. Über den Redis-Server wird der Status des Roboterarms übertragen. Der Redis-Server muss gestartet werden, bevor die Skripte ausgeführt werden.

```bash
docker run --rm --name redis -p 6379:6379 -v "$(pwd)/redis:/data" -d redis redis-server --save 60 1 --loglevel warning
```

## Benutzung

Aktivierung der virtuellen Umgebung in Linux / Unix:

```bash
source venv/bin/activate
```

Aktivierung der virtuellen Umgebung in Windows:

```bash
venv\Scripts\activate.bat
```

Ausführen der Skripte:

```bash
python simulation.py
python renderer.py
```
