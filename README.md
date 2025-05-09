# mks

Web-Application for improving presentation and organisation-system for schools of music.

## Powered with:
   
   - Python

## mks in action:
![Bildschirmfoto 2020-01-02 um 19 02 10](https://user-images.githubusercontent.com/40589021/71683419-ce6dd100-2d92-11ea-8d49-5d5cbff9154b.png)

![Bildschirmfoto 2020-01-02 um 19 07 00](https://user-images.githubusercontent.com/40589021/71683511-10971280-2d93-11ea-844f-5009618425ba.png)


## Idea:
Design, Frontend and Backup-Code is made by Lukas Schönsgibl (aka hybridpicker)

## Example Site:
https://www.musikschule-stp.at/

## Instructions:

mks loads all data from **fixtures** with the migrate-command:
```python
python manage.py migrate
```

### Git Hooks

Das Projekt verwendet Git-Hooks, um bestimmte Aufgaben zu automatisieren:

1. **Installation der Hooks**:
   ```bash
   ./install_git_hooks.sh
   ```

2. **pre-push Hook**:
   - Generiert automatisch ein aktuelles Fixture für die Dance-App vor jedem Push
   - Führt Tests aus, bevor ein Push erlaubt wird
   - Stellt sicher, dass die Dance-App-Daten immer synchronisiert sind

> **Hinweis**: Der pre-push Hook benötigt Zugriff auf die Django-Umgebung. Wenn du eine andere Umgebung als die Standardkonfiguration verwendest, passe die Umgebungspfade in der Datei `.git/hooks/pre-push` an.
