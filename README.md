# grades LSF Тool

Ein CLI Tool um sich Noten aus einem LSF System (Fernuni Hagen) anzeigen zu lassen.

## Installation

Python 3 und pip3 werden benötigt.

```bash
sudo apt install python3-pip
```

```bash
git clone https://github.com/nidzov/grades.git
```

```bash
cd ./grades
```

```bash
pip3 install --user --editable .
```

Im Terminal grades eingeben und ausführen.

## Beispiele

```
$ grades --help
Usage: grades [OPTIONS] [SEARCH_STRING]...

Options:
  -p, --passed       Zeigt nur bestandene Fächer an (Note >= 4,0).
  -c, --credentials  Benutzername und Passwort erneut eingeben.
  -s, --statistic    Gibt die Notenstatistik zu einzelnem Fach an.
  --help             Show this message and exit.
```

<img src="https://github.com/ndz-v/grades/blob/master/media/examples1.png" width="600">

### Notensatistik ausgeben

<img src="https://github.com/ndz-v/grades/blob/master/media/examples2.png" width="600">
